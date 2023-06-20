import math

from fastapi import APIRouter, Depends
from pydantic import BaseModel, validator
from tortoise.exceptions import IntegrityError

from backend.database.models import Roles
from backend.responses import BaseResponse
from backend.responses.error import Conflict, NotFound
from backend.responses.roles import GetRolesResponse
from backend.utils import Permissions, TokenJwt, validate_token

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/")
async def get_role(
    page: int,
    permissions: Permissions = None,
    token: TokenJwt = Depends(validate_token),
):
    roles = (
        Roles.filter(permissions=permissions) if permissions else Roles
    ).all()
    roles_list = await roles.offset((page - 1) * 10).limit(10).values()

    return GetRolesResponse(
        roles=roles_list, pages=math.ceil(await roles.count() / 10)
    )


class AddRoleItem(BaseModel):
    name: str
    permissions: Permissions

    @validator("name")
    def validate_name_length(cls, name):
        if not name:
            raise ValueError("The 'name' field can not be empty.")

        if len(name) > 20:
            raise ValueError(
                "The 'name' field must have a maximum length of 20 characters."
            )

        return name

    class Config:
        smart_union = True


@router.post("/")
async def add_role(
    item: AddRoleItem, token: TokenJwt = Depends(validate_token)
):
    try:
        await Roles.create(name=item.name, permissions=item.permissions)

        return BaseResponse()
    except IntegrityError:
        raise Conflict("existing product")


@router.delete("/{role_id}")
async def remove_role(role_id: int, token: TokenJwt = Depends(validate_token)):
    role = await Roles.get_or_none(id=role_id)

    if not role:
        raise NotFound("Role not exist")

    await role.delete()

    return BaseResponse()