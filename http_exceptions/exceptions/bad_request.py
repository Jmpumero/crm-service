class BadRequestException(Exception):
    def __init__(self, message: str = "Bad Request") -> None:
        self.message: str = message
        self.status_code = 400
