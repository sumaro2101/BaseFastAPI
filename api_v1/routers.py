from fastapi import FastAPI

from config import settings
from api_v1.users.views import router


def register_routers(app: FastAPI) -> None:
    app.include_router(
        router=router,
        prefix=settings.API_PREFIX,
        )
