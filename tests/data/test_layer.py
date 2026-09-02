from unittest.mock import MagicMock

from rootcast.data.layer import DataLayer
from rootcast.data.providers.massive import MassiveClient


def test_data_layer_uses_provided_massive_client():
    fake = MagicMock(spec=MassiveClient)

    layer = DataLayer(massive=fake)

    assert layer.massive is fake


def test_data_layer_defaults_to_env_configured_massive_client(monkeypatch):
    monkeypatch.setenv("MASSIVE_API_KEY", "env-key")

    layer = DataLayer()

    assert isinstance(layer.massive, MassiveClient)
    assert layer.massive.api_key == "env-key"
