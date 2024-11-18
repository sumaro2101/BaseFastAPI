from contextlib import asynccontextmanager
from fastapi import FastAPI

from config import db_connection, BaseModel
from api_v1 import register_routers
from logs import create_log_dirs



def start_app() -> FastAPI:
    """
    Создание приложения со всеми настройками
    """
    create_log_dirs()
    app = FastAPI(lifespan=lifespan)
    register_routers(app=app)
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_connection.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        yield
    await db_connection.dispose()


app = start_app()
