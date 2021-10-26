class UnauthorizedException(Exception):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__()
        self.message: str = message
        self.status_code = 401
