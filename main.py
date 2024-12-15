from contextlib import asynccontextmanager
from fastapi import FastAPI

from api_v1 import register_routers
from app_includes import (
    register_errors,
    register_middlewares,
    register_prometheus,
    )


def start_app() -> FastAPI:
    """
    Создание приложения со всеми настройками
    """
    app = FastAPI(lifespan=lifespan)
    register_routers(app=app)
    register_errors(app=app)
    register_middlewares(app=app)
    register_prometheus(app=app)
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = start_app()
