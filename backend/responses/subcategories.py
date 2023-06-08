from backend.responses import BaseResponse


class GetSubcategoriesResponse(BaseResponse):
    categories: list[dict | str]
