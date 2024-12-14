from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from .mixins import ActionUserManagerMixin, PasswordValidationMixin
from config.models import User
from config import settings
from config import db_connection


class UserManager(ActionUserManagerMixin,
                  PasswordValidationMixin,
                  IntegerIDMixin,
                  BaseUserManager[User, int]):
    """
    UserManager для работы с пользователем
    """

    verification_token_secret = settings.JWT.SECRET
    verification_token_audience = 'fastapi-users:auth'

    reset_password_token_secret = settings.JWT.SECRET
    reset_password_token_lifetime_seconds = settings.JWT.RESET_LIFESPAN_TOKEN_SECONDS


async def get_user_manager(session: AsyncSession = Depends(
    db_connection.session_geter,
)) -> UserManager:
    return UserManager(user_db=SQLAlchemyUserDatabase(
        session=session,
        user_table=User,
        ))
