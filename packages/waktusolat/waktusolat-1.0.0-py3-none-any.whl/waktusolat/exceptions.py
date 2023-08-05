class WaktuSolatBaseError(Exception):
    """Base class for all waktusolat-related errors"""


class APIError(Exception):
    """
    Raised if API returns an unsuccessful HTTP status code

    Args:
        msg (str): Human-readable string describing the error
        code (int): Status code returned by the API
    """

    def __init__(self, msg: str, code: int) -> None:
        self.msg = msg
        self.code = code

    def __str__(self):
        return f"{self.code} - {self.msg}"


class ConnectionError(WaktuSolatBaseError):
    """Raised when there are network problems"""
