class Error(Exception):
    pass


class UnauthUserError(Error):
    """Raised when the user hasn't entered their API information."""

    pass
