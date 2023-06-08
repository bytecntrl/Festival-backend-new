from argon2 import PasswordHasher
from argon2.exceptions import (
    HashingError,
    InvalidHash,
    VerificationError,
    VerifyMismatchError,
)
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from tortoise.exceptions import IntegrityError

from backend.database.models import Users
from backend.decorators import check_role
from backend.responses import BaseResponse
from backend.responses.auth import LoginResponse
from backend.responses.error import BadRequest, Conflict, Unauthorized
from backend.utils import Roles, TokenJwt, encode_jwt, validate_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
async def login(username: str, password: str):
    user = await Users.get_or_none(username=username).values()

    if not user:
        raise Unauthorized("Invalid username or password")

    try:
        ph = PasswordHasher()
        ph.verify(user["password"], password)

    except (VerificationError, VerifyMismatchError, HashingError, InvalidHash):
        raise Unauthorized("Invalid username or password")

    payload = TokenJwt(username, user["role"])

    return LoginResponse(token=encode_jwt(payload))


class RegisterItem(BaseModel):
    username: str
    password: str
    role: Roles


# admin: add new user
@router.post("/")
@check_role(Roles.ADMIN)
async def register(
    item: RegisterItem, token: TokenJwt = Depends(validate_token)
):
    if item.role == Roles.ADMIN:
        raise BadRequest("Unable to create admin user")

    if not item.username or not item.password:
        raise BadRequest("User or password missed")

    if not item.username.isalpha():
        raise BadRequest("The username has illegal characters")

    if len(item.password) >= 29 or len(item.username) >= 29:
        raise BadRequest("User or password too long")

    try:
        ph = PasswordHasher()

        user = Users(
            username=item.username,
            password=ph.hash(item.password),
            role=item.role.value,
        )

        await user.save()
    except IntegrityError:
        raise Conflict("User alredy exists")

    return BaseResponse()
