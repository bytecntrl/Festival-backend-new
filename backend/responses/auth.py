from pydantic import BaseModel


class LoginResponse(BaseModel):
    error: bool = False
    message: str = ""
    token: str
