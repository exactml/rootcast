# Copyright (C) Rootcast - All Rights Reserved

"""
Shared error hierarchy for rootcast.
"""


class RootcastError(Exception):
    """
    Base class for all rootcast errors.
    """


class DataProviderError(RootcastError):
    """
    Base class for errors raised by a data-provider client.
    """


class MissingCredentialsError(DataProviderError):
    """
    Raised when a provider client is missing required credentials.
    """


class AuthenticationError(DataProviderError):
    """
    Raised when a provider rejects credentials (e.g. HTTP 401).
    """


class ProviderAPIError(DataProviderError):
    """
    Raised when a provider returns an unexpected/error response.
    """


class ClientDisabledError(DataProviderError):
    """
    Raised when a client or one of its APIs is disabled in contract.yaml.
    """
