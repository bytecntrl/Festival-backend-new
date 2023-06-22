import functools

from backend.utils import Permissions, TokenJwt
from backend.responses.error import Forbidden


def check_role(*permission: Permissions):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(token: TokenJwt, *args, **kwargs):
            if token.permissions not in permission:
                raise Forbidden("Not allowed")

            return await func(token=token, *args, **kwargs)

        return wrapper

    return decorator
