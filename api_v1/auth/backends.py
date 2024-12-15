from fastapi_users.authentication import (
    BearerTransport,
    AuthenticationBackend,
    Authenticator,
    JWTStrategy,
    )

from api_v1.users.user_manager import get_user_manager
from config import settings


bearer_transport = BearerTransport(settings.CURRENT_ORIGIN +
                                   settings.API_PREFIX +
                                   settings.JWT.JWT_PATH +
                                   '/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.JWT.SECRET,
        lifetime_seconds=settings.JWT.RESET_LIFESPAN_TOKEN_SECONDS,
        )


auth_backend = AuthenticationBackend(
    name=settings.JWT.NAME,
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

authenticator = Authenticator(
    (auth_backend,),
    get_user_manager,
)
