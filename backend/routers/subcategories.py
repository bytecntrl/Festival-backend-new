import math

from fastapi import APIRouter, Depends
from pydantic import BaseModel, validator
from tortoise.exceptions import IntegrityError

from backend.database.models import Subcategories
from backend.decorators import check_role
from backend.responses import BaseResponse
from backend.responses.error import BadRequest, Conflict
from backend.responses.subcategories import (
    GetSubcategoriesListResponse,
    GetSubcategoriesResponse,
)
from backend.utils import Permissions, TokenJwt, validate_token

router = APIRouter(prefix="/subcategories", tags=["subcategories"])


# all: get subcategories
@router.get("/")
async def get_subcategories(
    page: int, token: TokenJwt = Depends(validate_token)
):
    categories = Subcategories.all()
    categories_list = (
        await categories.offset((page - 1) * 10)
        .limit(10)
        .order_by("order")
        .values()
    )

    return GetSubcategoriesResponse(
        categories=categories_list,
        pages=math.ceil(await categories.count() / 10),
    )


# all: get list subcategories
@router.get("/list")
async def get_list_subcategories(token: TokenJwt = Depends(validate_token)):
    categories = [x["name"] for x in await Subcategories.all().values()]

    return GetSubcategoriesListResponse(categories=categories)


class AddSubcategoriesItem(BaseModel):
    name: str
    order: int

    @validator("name")
    def validate_name_length(cls, name: str):
        if not name:
            raise ValueError("The 'name' field can not be empty.")

        if len(name) > 20:
            raise ValueError(
                "The 'name' field must have a maximum length of 20 characters."
            )

        return name


# admin: add subcategory
@router.post("/")
@check_role(Permissions.ALL)
async def add_subcategory(
    item: AddSubcategoriesItem, token: TokenJwt = Depends(validate_token)
):
    try:
        await Subcategories(name=item.name, order=item.order).save()
    except IntegrityError:
        raise Conflict("Existing subcategories")

    return BaseResponse()


# admin: delete category
@router.delete("/{subcategory_id}")
@check_role(Permissions.ALL)
async def delete_subcategory(
    subcategory_id: int, token: TokenJwt = Depends(validate_token)
):
    subcategory = Subcategories.filter(id=subcategory_id)

    if not await subcategory.exists():
        raise BadRequest("Subcategory not exist")

    await subcategory.delete()

    return BaseResponse()
