from argon2 import PasswordHasher
from argon2.exceptions import (
    HashingError,
    InvalidHash,
    VerificationError,
    VerifyMismatchError,
)
from fastapi import APIRouter

from backend.database.models import Users
from backend.responses.error import InvalidUsernameOrPassword
from backend.utils import TokenJwt, encode_jwt

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
async def login(username: str, password: str):
    user = await Users.get_or_none(username=username).values()

    if not user:
        raise InvalidUsernameOrPassword()

    try:
        ph = PasswordHasher()
        ph.verify(user["password"], password)

    except (VerificationError, VerifyMismatchError, HashingError, InvalidHash):
        raise InvalidUsernameOrPassword()

    payload = TokenJwt(username, user["role"])

    return {"error": False, "message": "", "token": encode_jwt(payload)}
