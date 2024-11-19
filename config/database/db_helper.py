from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    async_scoped_session,
                                    AsyncSession,
                                    )
from sqlalchemy.pool import Pool
from asyncio import current_task

from typing import AsyncGenerator, Any

from config import settings


DATA_BASE_URL = settings.db.url


class DataBaseHelper:
    """
    Вспомогательный класс для работы с Базой Данных
    """
    def __init__(self,
                 db_url: str = DATA_BASE_URL,
                 poolclass: Pool | None = None,
                 ) -> None:
        self._db_url = db_url
        setup = dict(
            url=self._db_url,
            echo=settings.debug,
        )
        if poolclass:
            setup.update(
                poolclass=poolclass,
            )
        self.engine = create_async_engine(
            **setup
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    def get_scoped_session(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session,
            scopefunc=current_task,
        )
        return session

    async def session_geter(self) -> AsyncGenerator[AsyncSession, Any]:
        session = self.get_scoped_session()
        yield session
        await session.remove()


db_helper = DataBaseHelper()
db_test = DataBaseHelper
