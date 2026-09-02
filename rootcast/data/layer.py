# Copyright (C) Rootcast - All Rights Reserved

"""Registry of configured data-provider clients."""

from __future__ import annotations

from rootcast.data.providers.massive import MassiveClient


class DataLayer:
    def __init__(
        self,
        massive: MassiveClient | None = None,
    ) -> None:
        """Configure the registry, defaulting to a client built from the environment."""
        self.massive = massive or MassiveClient()
