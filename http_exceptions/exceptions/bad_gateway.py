class BadGatewayException(Exception):
    def __init__(self, message="Bad Gateway") -> None:
        self.message = message
        self.status_code = 502
