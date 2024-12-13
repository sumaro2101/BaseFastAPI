from typing import Any
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from .user_manager import get_user_manager


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
    ):
        token = request.headers.get('Authorization')
        manager = await get_user_manager()
        user = await manager.authenticate_user(token)
        request.scope['user'] = user
        response = await call_next(request)
        return response
