from fastapi_users.authentication import (
    BearerTransport,
    AuthenticationBackend,
    JWTStrategy,
    )

from config import settings


bearer_transport = BearerTransport()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT.SECRET,
                       lifetime_seconds=settings.JWT.RESET_LIFESPAN_TOKEN_SECONDS,
                       )


auth_backend = AuthenticationBackend(
    name=settings.JWT.NAME,
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
