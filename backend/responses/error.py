from fastapi import status


class UnicornException(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message


class InvalidUsernameOrPassword(UnicornException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED, "Invalid username or password"
        )
