class MeetCallbackError(Exception):
    """Base exception for Meet Callback errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class GoogleClientError(MeetCallbackError):
    """Exception raised for errors in the Google Client operations."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ConfigurationError(MeetCallbackError):
    """Exception raised for configuration-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
