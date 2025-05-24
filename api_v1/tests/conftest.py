import httpx
import pytest_asyncio
import pytest

from typing import Any, AsyncGenerator
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from sqlalchemy.pool import NullPool

from config import test_connection, settings
from config import db_connection
from config.models.base import Base
from main import app


db_setup = test_connection(
    settings.test_db.url,
    poolclass=NullPool,
)


async def override_get_async_session():
    async with db_setup.session() as session:
        yield session


@pytest_asyncio.fixture(scope='session', autouse=True)
async def test_app() -> AsyncGenerator[LifespanManager, Any]:
    app.dependency_overrides[db_connection.session_geter] = override_get_async_session

    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture(scope='session')
async def client(test_app: FastAPI) -> AsyncGenerator[httpx.AsyncClient, Any]:
    current_home = settings.CURRENT_ORIGIN
    current_api = settings.API_PREFIX
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(
            app=app,
            ),
        base_url=current_home + current_api,
    ) as client:
        async with db_setup.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield client
        async with db_setup.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def get_async_session():
    async with db_setup.session() as session:
        yield session


@pytest.fixture()
def user_test_data():
    data = {
        "email": "user@example.com",
        "password": "password",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    }
    return data
