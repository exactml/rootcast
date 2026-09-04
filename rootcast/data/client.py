# Copyright (C) Rootcast - All Rights Reserved

"""
Ancestor class for data-provider REST clients.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import requests
import yaml

from rootcast.errors import AuthenticationError, ClientDisabledError, ProviderAPIError

_CONTRACT_PATH = Path(__file__).parent / "contract.yaml"


@lru_cache(maxsize=1)
def _load_contract() -> dict[str, Any]:
    """
    Load and cache contract.yaml.
    """
    with _CONTRACT_PATH.open() as f:
        return yaml.safe_load(f)


class BaseClient:
    """
    Shared request/error handling for provider clients.

    Subclasses set `base_url` and implement `_headers()`. Other transports
    (POST, websocket) can be added here later without touching subclasses.
    """

    base_url: str

    @classmethod
    def load_contract(cls, client_name: str) -> dict[str, Any]:
        """
        Return the contract.yaml section for one client, by name.
        """
        return _load_contract()["clients"][client_name]

    def __init__(
        self,
        session: requests.Session | None = None,
    ) -> None:
        """
        Initialize the client with an HTTP session.
        """
        self.session = session or requests.Session()

    def _headers(self) -> dict[str, str]:
        """
        Return the auth headers for a request; subclasses must override.
        """
        raise NotImplementedError

    def _require_enabled(
        self,
        section: dict[str, Any],
        name: str,
    ) -> None:
        """
        Raise ClientDisabledError if the given contract section is disabled.
        """
        if not section.get("enabled", True):
            raise ClientDisabledError(f"{name} is disabled in contract.yaml.")

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Send a GET request and return the decoded JSON response body.
        """
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        response = self.session.get(
            url, params=params, headers=self._headers(), timeout=30
        )
        if response.status_code == 401:
            raise AuthenticationError(
                f"{type(self).__name__} rejected credentials (401)."
            )
        if not response.ok:
            raise ProviderAPIError(
                f"{type(self).__name__} request failed: "
                f"{response.status_code} {response.text}"
            )
        return response.json()
