class BadRequestException(Exception):
    def __init__(self, message="Bad Request") -> None:
        self.message = message
        self.status_code = 400
