"""Integration tests that hit the real Massive API.

Skipped unless MASSIVE_API_KEY is set, so they don't run in environments
without a key (e.g. CI without a configured secret).
"""

import os
import pdb

import pytest

from rootcast.data.providers.massive import MassiveClient

pytestmark = pytest.mark.skipif(
    not os.environ.get("MASSIVE_API_KEY"),
    reason="requires a live MASSIVE_API_KEY",
)


def test_list_tickers_live_returns_aapl_reference_data():
    client = MassiveClient()

    tickers = list(client.list_tickers(market="stocks", ticker="AAPL"))

    import pdb; pdb.set_trace()

    assert len(tickers) == 1
    aapl = tickers[0]
    assert aapl["ticker"] == "AAPL"
    assert aapl["active"] is True
    assert aapl["market"] == "stocks"
    assert aapl["name"]
    assert aapl["primary_exchange"]
