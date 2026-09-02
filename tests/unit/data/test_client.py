# Copyright (C) Rootcast - All Rights Reserved

from unittest.mock import MagicMock

import pytest
import requests

from rootcast.data.client import BaseClient
from rootcast.errors import AuthenticationError, ProviderAPIError


class _DummyClient(BaseClient):
    base_url = "https://example.test"

    def _headers(self) -> dict[str, str]:
        return {"Authorization": "Bearer dummy"}


def make_response(
    status_code: int,
    payload: dict | None = None,
) -> MagicMock:
    response = MagicMock(spec=requests.Response)
    response.status_code = status_code
    response.ok = status_code < 400
    response.text = "error body"
    response.json.return_value = payload or {}
    return response


def test_get_returns_json_on_success():
    session = MagicMock()
    session.get.return_value = make_response(200, {"hello": "world"})

    client = _DummyClient(session=session)
    result = client.get("/ping")

    assert result == {"hello": "world"}
    session.get.assert_called_once_with(
        "https://example.test/ping",
        params=None,
        headers={"Authorization": "Bearer dummy"},
        timeout=30,
    )


def test_get_uses_absolute_path_as_is():
    session = MagicMock()
    session.get.return_value = make_response(200, {})

    client = _DummyClient(session=session)
    client.get("https://example.test/ping?cursor=abc")

    session.get.assert_called_once_with(
        "https://example.test/ping?cursor=abc",
        params=None,
        headers={"Authorization": "Bearer dummy"},
        timeout=30,
    )


def test_get_raises_authentication_error_on_401():
    session = MagicMock()
    session.get.return_value = make_response(401)

    client = _DummyClient(session=session)
    with pytest.raises(AuthenticationError):
        client.get("/ping")


def test_get_raises_provider_api_error_on_other_failure():
    session = MagicMock()
    session.get.return_value = make_response(500)

    client = _DummyClient(session=session)
    with pytest.raises(ProviderAPIError):
        client.get("/ping")


def test_load_contract_returns_massive_section():
    contract = BaseClient.load_contract("massive")

    assert contract["base_url"] == "https://api.massive.com"
    assert "list_tickers" in contract["apis"]
