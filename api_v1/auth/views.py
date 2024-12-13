from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from config.models import User
from config import settings
from .backends import auth_backend
from .schemas import UserRead, UserCreate, UserUpdate
from api_v1.users.user_manager import get_user_manager


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    (auth_backend,)
)


router = APIRouter()
router.include_router(fastapi_users.get_auth_router(auth_backend),
                      tags=['Auth'],
                      prefix=settings.JWT.JWT_PATH,
                      )
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate),
                      tags=['Auth'],
                      prefix='/auth',
                      )
router.include_router(fastapi_users.get_verify_router(UserRead),
                      tags=['Auth'],
                      prefix='/auth',
                      )
router.include_router(fastapi_users.get_reset_password_router(),
                      tags=['Auth'],
                      prefix='/auth',
                      )
router.include_router(fastapi_users.get_reset_password_router(),
                      tags=['Auth'],
                      prefix='/auth',
                      )
router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate),
                      tags=['Users'],
                      prefix='/users',
                      )
