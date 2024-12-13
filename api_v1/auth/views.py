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


router = APIRouter(tags=['Auth'],
                   )
router.include_router(fastapi_users.get_auth_router(auth_backend),
                      prefix=settings.JWT.JWT_PATH,
                      )
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate),
                      prefix='/auth',
                      )
router.include_router(fastapi_users.get_verify_router(UserRead),
                      prefix='/auth',
                      )
router.include_router(fastapi_users.get_reset_password_router(),
                      prefix='/auth',
                      )
router.include_router(fastapi_users.get_reset_password_router(),
                      prefix='/auth',
                      )
router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate),
                      prefix='/auth',
                      )
