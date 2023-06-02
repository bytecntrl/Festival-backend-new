from fastapi import APIRouter

from backend.responses.error import InvalidUsernameOrPassword

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
async def login(username: str, password: str):
    raise InvalidUsernameOrPassword()
