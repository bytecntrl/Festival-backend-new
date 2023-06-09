import math

from argon2 import PasswordHasher
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.database.models import Users
from backend.decorators import check_role
from backend.responses import BaseResponse
from backend.responses.error import Forbidden, NotFound
from backend.responses.users import GetUserResponse, GetUsersResponse
from backend.utils import Roles, TokenJwt, validate_token

router = APIRouter(prefix="/users", tags=["users"])


# admin: get list of user
@router.get("/")
@check_role(Roles.ADMIN)
async def get_users(page: int, token: TokenJwt = Depends(validate_token)):
    users = Users.all().exclude(role=Roles.ADMIN)
    list_users = (
        await users.offset((page - 1) * 10)
        .limit(10)
        .values("id", "username", "role")
    )

    return GetUsersResponse(
        users=list_users, pages=math.ceil(await users.count() / 10)
    )


# all: get user information
@router.get("/{username}")
async def get_user_admin(
    username: str, token: TokenJwt = Depends(validate_token)
):
    user = await Users.get_or_none(username=username)

    if not user:
        raise NotFound("Invalid username")

    if not (token.role == "admin" or token.username == username):
        raise Forbidden("Not allowed")

    return GetUserResponse(user=await user.to_dict())


class ChangePasswordItem(BaseModel):
    password: str


# all: change password of user
@router.put("/")
async def change_password(
    item: ChangePasswordItem, token: TokenJwt = Depends(validate_token)
):
    ph = PasswordHasher()

    await Users.filter(username=token.username).update(
        password=ph.hash(item.password)
    )

    return BaseResponse()


# admin: delete user
@router.delete("/{user_id}")
@check_role(Roles.ADMIN)
async def delete_user(user_id: int, token: TokenJwt = Depends(validate_token)):
    user = await Users.get_or_none(id=user_id)

    if not user:
        raise NotFound("User not exist")

    if user.role == Roles.ADMIN:
        raise Forbidden("You cannot delete an admin")

    await user.delete()

    return BaseResponse()
