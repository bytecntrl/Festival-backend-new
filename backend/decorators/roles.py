import functools

from backend.utils import Roles, TokenJwt
from backend.responses.error import Forbidden


def check_role(*roles: Roles):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(token: TokenJwt, *args, **kwargs):
            if token.role not in roles:
                raise Forbidden("Not allowed")

            return await func(token=token, *args, **kwargs)

        return wrapper

    return decorator
