from fastapi import APIRouter, Depends
from pydantic import BaseModel
from tortoise.exceptions import IntegrityError

from backend.database.models import Products, Subcategories
from backend.decorators import check_role
from backend.responses.error import BadRequest, Conflict
from backend.utils import Category, TokenJwt, validate_token
from backend.responses import BaseResponse

router = APIRouter(prefix="/products", tags=["products"])


class AddProductItem(BaseModel):
    name: str
    short_name: str
    is_priority: bool
    price: float
    category: Category
    subcategory: int

    class Config:
        smart_union = True


# admin: add product
@router.post("/")
@check_role("admin")
async def add_product(
    item: AddProductItem, token: TokenJwt = Depends(validate_token)
):
    if not item.name or len(item.name) >= 30:
        raise BadRequest("Wrong name")

    if not item.short_name or len(item.short_name) >= 15:
        raise BadRequest("Wrong short_name")

    if item.price <= 0:
        raise BadRequest("Wrong price")

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
