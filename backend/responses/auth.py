from backend.responses import BaseResponse


class LoginResponse(BaseResponse):
    token: str


class RegisterResponse(BaseResponse):
    user: dict
