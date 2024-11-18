from fastapi import FastAPI

from config import settings
from api_v1.users.views import router as users


def register_routers(app: FastAPI) -> None:
    app.include_router(
        router=users,
        prefix=settings.API_PREFIX,
        )
