class UnauthorizedException(Exception):
    def __init__(self, message="Unauthorized") -> None:
        self.message = message
        self.status_code = 401
