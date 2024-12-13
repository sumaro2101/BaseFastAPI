from typing import Any
from fastapi import Request, Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from .user_manager import UserManager
from config.models import User
from config import db_connection


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Прослойка которая добавляет User в Request
    """
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Any,
        session: AsyncSession = Depends(db_connection.session_geter),
    ):
        token = request.headers.get('Authorization')
        user_db = SQLAlchemyUserDatabase(session, User)
        manager = UserManager(user_db=user_db)
        user = await manager.authenticate_user(token)
        request.scope['user'] = user
        response = await call_next(request)
        return response
