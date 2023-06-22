from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, validator
from tortoise.exceptions import IntegrityError

from backend.database.models import Products, Subcategories
from backend.decorators import check_role
from backend.responses import BaseResponse
from backend.responses.error import BadRequest, Conflict
from backend.utils import Category, Permissions, TokenJwt, validate_token

router = APIRouter(prefix="/products", tags=["products"])


class AddProductItem(BaseModel):
    name: str
    short_name: str
    is_priority: bool
    price: float = Field(ge=0)
    category: Category
    subcategory: int

    @validator("name")
    def validate_name_length(cls, name):
        if len(name) > 30:
            raise ValueError(
                "The 'name' field must have a maximum length of 30 characters."
            )
        return name

    @validator("short_name")
    def validate_short_name_length(cls, short_name):
        if len(short_name) > 15:
            raise ValueError(
                "The 'short_name' field must have a maximum length of 15 characters."
            )
        return short_name

    class Config:
        smart_union = True
        strict = True


# admin: add product
@router.post("/")
@check_role(Permissions.ALL)
async def add_product(
    item: AddProductItem, token: TokenJwt = Depends(validate_token)
):
    try:
        s = await Subcategories.get_or_none(id=item.subcategory)
        if not s:
            raise BadRequest("subcategory nonexistent")

        await Products.create(
            name=item.name,
            short_name=item.short_name,
            is_priority=item.is_priority,
            price=item.price,
            category=item.category,
            subcategory=s,
        )

        return BaseResponse()

    except IntegrityError:
        raise Conflict("existing product")
