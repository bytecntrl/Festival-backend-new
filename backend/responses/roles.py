from backend.responses import BaseResponse


class GetRolesResponse(BaseResponse):
    roles: list[dict]
    pages: int


class GetRolesNameResponse(BaseResponse):
    roles: dict[int, str]
