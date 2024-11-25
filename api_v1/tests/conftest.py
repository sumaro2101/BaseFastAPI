import asyncio
import httpx
import pytest_asyncio
import pytest

from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from sqlalchemy.pool import NullPool
from alembic.config import Config
from alembic import command

from config import test_connection, settings, BaseModel
from config import db_connection
from api_v1.routers import register_routers


db_setup = test_connection(
    settings.test_db.url,
    poolclass=NullPool,
)


cfg = Config(settings.alembic.CONFIG_PATH.as_posix())
cfg.set_main_option('script_location',
                    settings.alembic.MIGRATION_PATH.as_posix(),
                    )


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def override_get_async_session():
    async with db_setup.session() as session:
        yield session


@pytest_asyncio.fixture(scope='session', autouse=True)
async def app() -> AsyncGenerator[LifespanManager, Any]:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with db_setup.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)
            await conn.run_sync(alembic_do_upgrade)
            yield
            await conn.run_sync(BaseModel.metadata.drop_all)

    app = FastAPI(docs_url=None,
                  redoc_url=None,
                  lifespan=lifespan,
                  )
    register_routers(app=app)
    app.dependency_overrides[db_connection.session_geter] = override_get_async_session

    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture(scope='session')
async def client(app: FastAPI) -> AsyncGenerator[httpx.AsyncClient, Any]:
    current_home = settings.CURRENT_ORIGIN
    current_api = settings.API_PREFIX
    async with httpx.AsyncClient(
        app=app,
        base_url=current_home + current_api,
    ) as client:
        yield client


def alembic_do_upgrade(connection):
    """
    Upgrade миграция алембик
    """
    cfg.attributes['connection'] = connection
    command.upgrade(cfg, 'head')
