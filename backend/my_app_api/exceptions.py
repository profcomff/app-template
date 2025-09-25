class APIError(Exception):
    """Base class for API errors"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
