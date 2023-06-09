from backend.responses import BaseResponse


class GetUsersResponse(BaseResponse):
    users: list[dict]
    pages: int


class GetUserResponse(BaseResponse):
    user: dict
