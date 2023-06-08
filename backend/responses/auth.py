from backend.responses import BaseResponse


class LoginResponse(BaseResponse):
    token: str
