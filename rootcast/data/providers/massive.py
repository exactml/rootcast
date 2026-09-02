"""Client for the Massive (massive.com) market data REST API."""

from __future__ import annotations

import os
from typing import Any, Iterator

import requests

from rootcast.data.base_client import BaseClient
from rootcast.errors import MissingCredentialsError


class MassiveClient(BaseClient):
    base_url = "https://api.massive.com"

    def __init__(
        self,
        api_key: str | None = None,
        session: requests.Session | None = None,
    ) -> None:
        super().__init__(session=session)
        self.api_key = api_key or os.environ.get("MASSIVE_API_KEY")
        if not self.api_key:
            raise MissingCredentialsError(
                "No Massive API key found. Pass api_key= or set MASSIVE_API_KEY."
            )

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def list_tickers(
        self,
        *,
        market: str = "stocks",
        active: bool = True,
        limit: int = 1000,
        **filters: Any,
    ) -> Iterator[dict[str, Any]]:
        """Yield ticker reference records, paginating through every result page."""
        params: dict[str, Any] | None = {
            "market": market,
            "active": active,
            "limit": limit,
            **filters,
        }
        url: str | None = "/v3/reference/tickers"
        while url:
            payload = self.get(url, params=params)
            yield from payload.get("results", [])
            url = payload.get("next_url")
            params = None
