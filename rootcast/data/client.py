"""Ancestor class for data-provider REST clients."""

from __future__ import annotations

from typing import Any

import requests

from rootcast.errors import AuthenticationError, ProviderAPIError


class BaseClient:
    """Shared request/error handling for provider clients.

    Subclasses set `base_url` and implement `_headers()`. Other transports
    (POST, websocket) can be added here later without touching subclasses.
    """

    base_url: str

    def __init__(self, session: requests.Session | None = None) -> None:
        self.session = session or requests.Session()

    def _headers(self) -> dict[str, str]:
        raise NotImplementedError

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
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
