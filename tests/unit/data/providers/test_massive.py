from unittest.mock import MagicMock

import pytest
import requests

from rootcast.data.providers.massive import MassiveClient
from rootcast.errors import AuthenticationError, MissingCredentialsError

BASE_URL = MassiveClient.base_url


def make_response(status_code: int, payload: dict | None = None) -> MagicMock:
    response = MagicMock(spec=requests.Response)
    response.status_code = status_code
    response.ok = status_code < 400
    response.text = "error body"
    response.json.return_value = payload or {}
    return response


def test_requires_api_key(monkeypatch):
    monkeypatch.delenv("MASSIVE_API_KEY", raising=False)
    with pytest.raises(MissingCredentialsError):
        MassiveClient()


def test_reads_api_key_from_env(monkeypatch):
    monkeypatch.setenv("MASSIVE_API_KEY", "env-key")
    client = MassiveClient()
    assert client.api_key == "env-key"


def test_list_tickers_sends_auth_header_and_params():
    session = MagicMock()
    session.get.return_value = make_response(200, {"results": [], "next_url": None})

    client = MassiveClient(api_key="test-key", session=session)
    list(client.list_tickers(market="stocks", active=True))

    session.get.assert_called_once_with(
        f"{BASE_URL}/v3/reference/tickers",
        params={"market": "stocks", "active": True, "limit": 1000},
        headers={"Authorization": "Bearer test-key"},
        timeout=30,
    )


def test_list_tickers_paginates_through_next_url():
    session = MagicMock()
    session.get.side_effect = [
        make_response(
            200,
            {
                "results": [{"ticker": "AAPL"}],
                "next_url": f"{BASE_URL}/v3/reference/tickers?cursor=abc",
            },
        ),
        make_response(200, {"results": [{"ticker": "MSFT"}], "next_url": None}),
    ]

    client = MassiveClient(api_key="test-key", session=session)
    tickers = list(client.list_tickers())

    assert [t["ticker"] for t in tickers] == ["AAPL", "MSFT"]
    assert session.get.call_count == 2
    second_call = session.get.call_args_list[1]
    assert second_call.args[0] == f"{BASE_URL}/v3/reference/tickers?cursor=abc"
    assert second_call.kwargs["params"] is None


def test_list_tickers_raises_on_401():
    session = MagicMock()
    session.get.return_value = make_response(401, {})

    client = MassiveClient(api_key="bad-key", session=session)
    with pytest.raises(AuthenticationError):
        list(client.list_tickers())
