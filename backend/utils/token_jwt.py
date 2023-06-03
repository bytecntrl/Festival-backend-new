import dataclasses
import datetime

import jwt
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidAlgorithmError,
    InvalidIssuedAtError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)

from backend.config import Session


@dataclasses.dataclass
class TokenJwt:
    username: str
    role: str
    exp: int = None

    def to_dict(self):
        return dict(username=self.username, role=self.role, exp=self.exp)


def encode_jwt(payload: TokenJwt) -> str:
    payload.exp = datetime.datetime.now(
        tz=datetime.timezone.utc
    ) + datetime.timedelta(seconds=Session.config.JWT_TOKEN_EXPIRES)

    return jwt.encode(
        payload.to_dict(), Session.config.JWT_SECRET, algorithm="HS256"
    )


def decode_jwt(token: str) -> TokenJwt | None:
    try:
        result = jwt.decode(
            token, Session.config.JWT_SECRET, algorithms=["HS256"]
        )

        return TokenJwt(**result)
    except (
        InvalidTokenError,
        DecodeError,
        InvalidSignatureError,
        ExpiredSignatureError,
        InvalidIssuedAtError,
        InvalidKeyError,
        InvalidAlgorithmError,
        MissingRequiredClaimError,
    ):
        return None