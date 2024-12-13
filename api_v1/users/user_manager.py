from fastapi_users import BaseUserManager, IntegerIDMixin

from .mixins import AuthenticationUserManagerMixin, PasswordValidationMixin
from config.models import User
from config import settings


class UserManager(AuthenticationUserManagerMixin,
                  PasswordValidationMixin,
                  IntegerIDMixin,
                  BaseUserManager[User, int]):
    """
    UserManager для работы с пользователем
    """

    verification_token_secret = settings.JWT.SECRET
    reset_password_token_lifetime_seconds = settings.JWT.RESET_LIFESPAN_TOKEN_SECONDS
