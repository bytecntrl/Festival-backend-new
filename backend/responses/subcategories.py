from backend.responses import BaseResponse


class GetSubcategoriesResponse(BaseResponse):
    categories: list[dict]
    pages: int


class GetSubcategoriesListResponse(BaseResponse):
    categories: list[str]
