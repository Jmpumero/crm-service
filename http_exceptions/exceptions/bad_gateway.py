class BadGatewayException(Exception):
    def __init__(self, message: str = "Bad Gateway") -> None:
        self.message: str = message
        self.status_code = 502
