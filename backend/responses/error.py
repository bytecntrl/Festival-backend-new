from fastapi import status


class UnicornException(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message


class BadRequest(UnicornException):
    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class Unauthorized(UnicornException):
    def __init__(self, message: str):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message)


class Forbidden(UnicornException):
    def __init__(self, message: str):
        super().__init__(status.HTTP_403_FORBIDDEN, message)


class Conflict(UnicornException):
    def __init__(self, message: str):
        super().__init__(status.HTTP_409_CONFLICT, message)
