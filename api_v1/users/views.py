from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers

from config.models import User
from api_v1.auth.backends import auth_backend
from api_v1.auth import active_user
from api_v1.auth.schemas import UserRead, UserUpdate
from api_v1.users.user_manager import get_user_manager


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    (auth_backend,)
)


router = APIRouter()


@router.get(path='/test',
            response_model=UserRead,
            dependencies=[Depends(active_user)],
            )
async def test_end_point(user: User = Depends(active_user)):
    return user


router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate),
                      tags=['Users'],
                      prefix='/users',
                      )
