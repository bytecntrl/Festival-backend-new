from argon2 import PasswordHasher
from argon2.exceptions import (
    HashingError,
    InvalidHash,
    VerificationError,
    VerifyMismatchError,
)
from fastapi import APIRouter, Depends
from pydantic import BaseModel, validator
from tortoise.exceptions import IntegrityError

from backend.database.models import Roles, Users
from backend.decorators import check_role
from backend.responses.auth import LoginResponse, RegisterResponse
from backend.responses.error import (
    BadRequest,
    Conflict,
    NotFound,
    Unauthorized,
)
from backend.utils import TokenJwt, encode_jwt, validate_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
async def login(username: str, password: str):
    user = await Users.get_or_none(username=username)

    if not user:
        raise Unauthorized("Invalid username or password")

    try:
        ph = PasswordHasher()
        ph.verify(user.password, password)

    except (VerificationError, VerifyMismatchError, HashingError, InvalidHash):
        raise Unauthorized("Invalid username or password")

    payload = TokenJwt(username, (await user.role).name)

    return LoginResponse(token=encode_jwt(payload))


class RegisterItem(BaseModel):
    username: str
    password: str
    role_id: int

    @validator("username")
    def validate_username_length(cls, username: str):
        if not username:
            raise ValueError("The 'username' field can not be empty.")

        if len(username) > 30:
            raise ValueError(
                "The 'username' field must have a maximum length of 30 characters."
            )

        if not username.isalpha():
            raise ValueError("The 'username' field has illegal characters.")

        return username

    @validator("password")
    def validate_password_length(cls, password: str):
        if not password:
            raise ValueError("The 'password' field can not be empty.")

        if len(password) > 30:
            raise ValueError(
                "The 'password' field must have a maximum length of 30 characters."
            )

        return password


# admin: add new user
@router.post("/")
@check_role("admin")
async def register(
    item: RegisterItem, token: TokenJwt = Depends(validate_token)
):
    role = await Roles.get_or_none(id=item.role_id)

    if not role:
        raise NotFound("Role not found.")

    if role.name == "admin":
        raise BadRequest("Unable to create admin user.")

    try:
        ph = PasswordHasher()

        user = Users(
            username=item.username,
            password=ph.hash(item.password),
            role=role,
        )

        await user.save()
    except IntegrityError:
        raise Conflict("User alredy exists.")

    return RegisterResponse(user=await user.to_dict())
