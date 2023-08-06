from __future__ import annotations
import signal
from urllib.parse import urljoin

import click
import requests
from requests import Response
from typing import List

from cloudtoken.core import utils
from cloudtoken.core.abstract_classes import CloudtokenPlugin
from cloudtoken.core.exceptions import (
    AuthenticationError,
    ConfigurationError,
)
from cloudtoken.core.helper_classes import CloudtokenOption
from cloudtoken.plugins.okta.enums import FactorResult, TransactionState
from cloudtoken.plugins.okta.exceptions import OktaError, UnsupportedFactorTypeError, UnsupportedTransactionStateError
from cloudtoken.plugins.okta.factors import handle_push_factor, handle_totp_factor


def binded_sigint_handler(plugin):
    def sigint_handler(signum, frame):
        # Clean up pending authentication on sigint
        # For example the user ctrl+c while entering TOTP
        if plugin._state_token:
            plugin.cancel_transaction()

    return sigint_handler


class Plugin(CloudtokenPlugin):
    name = "okta"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._ensure_required_config()

        self._session = requests.session()
        self._init_session_headers()
        self.last_response = None

        self._state_token = None
        self._transaction_state = None

        self._endpoint = self._get_plugin_config(["endpoint"])
        signal.signal(signal.SIGINT, binded_sigint_handler(self))

    def _ensure_required_config(self) -> None:
        required_fields = ["endpoint", "aws_app_name", "aws_app_id"]

        for field in required_fields:
            if not self._get_plugin_config([field]):
                raise ConfigurationError(f"Required configuration key '{field}' missing for okta plugin.")

    def _init_session_headers(self):
        self._session.headers.update({"CACHE-CONTROL": "no-cache"})
        self._session.headers.update({"User-Agent": f"Cloudtoken {utils.get_version()}"})

    def execute(self, data: dict) -> dict:
        if utils.existing_valid_saml_credentials(data):
            return data[self.name]
        while not self._is_at_end_state:
            handler = self._get_transaction_state_handler()
            # the next handler in the state machine often depends on
            # the response of the last handler
            self.last_response = handler()
            # extract error details and raise if there's an error
            # or bad response status
            self.check_response_and_raise(self.last_response)
            self._transaction_state = self.last_response.json()["status"]
        if self._transaction_state != TransactionState.Success:
            try:
                factor_result = self.last_response.json()["factorResult"]
            except (requests.JSONDecodeError, KeyError):
                factor_result = "n/a"
            raise AuthenticationError(f"failed with state {self._transaction_state} | factor result: {factor_result}")
        session_token = self.last_response.json()["sessionToken"]
        saml = self._get_saml_response(session_token)
        data = {"saml_response": saml}
        return data

    def primary_authentication_status(self):
        """First step in the authentication process.

        Docs: https://developer.okta.com/docs/reference/api/authn/#primary-authentication

        We are following the "Primary authentication with Public Application" flow.

        :return: Response instance
        :rtype: Response instance
        """
        auth_endpoint = urljoin(self._endpoint, "api/v1/authn")
        # Not sure if okta is going to use the system credentials like idapative.
        # Allow a way to override it with cli opt.
        username = self._get_plugin_config(["okta_user"]) or self._get_config(["username"])
        password = self._get_plugin_config(["okta_pass"]) or self._get_config(["password"])
        response = self._session.post(
            auth_endpoint, json={"username": username, "password": password, "options": self._auth_options}
        )
        self._state_token = response.json()["stateToken"]
        return response

    def mfa_required_status(self):
        """Handle MFA_REQUIRED status."""
        factors = self.last_response.json()["_embedded"]["factors"]
        preferred_factor_type = self._get_plugin_config(["mfa_method"])
        factor = None
        if preferred_factor_type:
            for f in factors:
                if f["factorType"] == preferred_factor_type:
                    factor = f
                    break
        # there is no preference or Okta didn't return the preference as an option
        if not factor:
            factor = self._select_supported_factor_or_raise(factors)
        response = self._session.post(factor["_links"]["verify"]["href"], json={"stateToken": self._state_token})
        return response

    def mfa_challenge_status(self):
        """Handle MFA_CHALLENGE status."""
        data = self.last_response.json()
        selected_factor = data["_embedded"]["factor"]
        next_link = data["_links"]["next"]["href"]
        handler = self._get_factor_handler(selected_factor["factorType"])
        return handler(self, next_link)

    def check_response_and_raise(self, response: Response):
        if response.ok:
            return
        try:
            data = response.json()
        except:
            response.raise_for_status()
        else:
            code = data.get("errorCode", "Unknown")
            summary = data.get("errorSummary", "Unknown")
            raise OktaError(f"okta error | code: {code} | summary: {summary}")

    @classmethod
    def options(cls) -> List[CloudtokenOption]:
        options = [
            cls.add_option(["--okta-user"], type=str, help="Username/email of your okta account"),
            cls.add_option(["--okta-pass"], type=str, help="Password for your okta account"),
            cls.add_option(["--mfa-passcode"], type=str, help="Specify the MFA passcode to use."),
            cls.add_option(
                ["--mfa-method"],
                type=click.Choice(["push", "token:software:totp"]),
                help="Specify the MFA method.",
            ),
        ]
        return options

    def cancel_transaction(self):
        data = self.last_response.json()
        try:
            cancel_link = data["_links"]["cancel"]["href"]
        except KeyError:
            pass
        else:
            self._session.post(cancel_link, json={"stateToken": self._state_token})

    @property
    def _auth_options(self):
        # https://developer.okta.com/docs/reference/api/authn/#options-object
        return {"multiOptionalFactorEnroll": "false", "warnBeforePasswordExpired": "false"}

    @property
    def _is_at_end_state(self):
        if self._transaction_state == TransactionState.Success:
            return True
        if self._transaction_state == TransactionState.MfaChallenge:
            factor_result = self.last_response.json().get("factorResult")
            return factor_result in [FactorResult.Rejected, FactorResult.Timeout, FactorResult.Cancelled]
        return False

    def _get_transaction_state_handler(self):
        try:
            return {
                None: self.primary_authentication_status,
                TransactionState.MfaRequired: self.mfa_required_status,
                TransactionState.MfaChallenge: self.mfa_challenge_status,
            }[self._transaction_state]
        except KeyError:
            raise UnsupportedTransactionStateError(f"transaction state not supported: {self._transaction_state}")

    def _select_supported_factor_or_raise(self, factors):
        choices = []
        for f in factors:
            choices.append(f["factorType"])
            try:
                self._get_factor_handler(f["factorType"])
            except UnsupportedFactorTypeError:
                pass
            else:
                return f
        raise UnsupportedFactorTypeError(f"Unable to find supported second factor, options: {','.join(choices)}")

    def _get_factor_handler(self, factor_type):
        try:
            return {"push": handle_push_factor, "token:software:totp": handle_totp_factor}[factor_type]
        except KeyError:
            raise UnsupportedFactorTypeError(f"factor type {factor_type} is unsupported")

    def _get_saml_response(self, session_token):
        app_name = self._get_plugin_config(["aws_app_name"])
        app_id = self._get_plugin_config(["aws_app_id"])
        response = self._session.get(f"{self._endpoint}/app/{app_name}/{app_id}/sso/saml?sessionToken={session_token}")
        return utils.get_saml_response_from_html(response.content)
