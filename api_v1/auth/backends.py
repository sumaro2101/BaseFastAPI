from fastapi_users.authentication import (
    BearerTransport,
    AuthenticationBackend,
    JWTStrategy,
    )

from config import settings


bearer_transport = BearerTransport()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET)
