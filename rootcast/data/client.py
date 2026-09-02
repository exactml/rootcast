# Copyright (C) Rootcast - All Rights Reserved

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

    def __init__(
        self,
        session: requests.Session | None = None,
    ) -> None:
        """Initialize the client with an HTTP session."""
        self.session = session or requests.Session()

    def _headers(self) -> dict[str, str]:
        """Return the auth headers for a request; subclasses must override."""
        raise NotImplementedError

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a GET request and return the decoded JSON response body."""
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
