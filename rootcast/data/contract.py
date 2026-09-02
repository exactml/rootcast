# Copyright (C) Rootcast - All Rights Reserved

"""
Loader for rootcast/data/contract.yaml.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_CONTRACT_PATH = Path(__file__).parent / "contract.yaml"


@lru_cache(maxsize=1)
def load_contract() -> dict[str, Any]:
    """
    Load and cache contract.yaml.
    """
    with _CONTRACT_PATH.open() as f:
        return yaml.safe_load(f)


def client_contract(client_name: str) -> dict[str, Any]:
    """
    Return the contract section for one client, by name.
    """
    return load_contract()["clients"][client_name]
