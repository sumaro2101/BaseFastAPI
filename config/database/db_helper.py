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
    Вспомогательный класс для работы с Базой Данных.

    Помогает инициализировать соединение с Базой Данных, а так же
    работу с сессиями.

    ## Инициализация:
        :string:`db_url` - Адресс базы данных.
        :string:`poolclass` - Пул типа :class:`sqlalchemy.pool.Pool`

    ## Методы:
        :function:`DataBaseHelper.session_geter` - Получение генератора текущей сессии.
        :function:`DataBaseHelper.get_scoped_session` - Получение текущей сессии.
        :function:`DataBaseHelper.dispose` - Закрытые соединения.

    ## Примеры:
    ```python
    from fastapi import FastAPI
    from contextlib import asynccontextmanager
    from config import db_connection, BaseModel


    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Инициализация соединения для создания таблиц.
        async with db_connection.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)
            yield
        await db_connection.dispose()

    app = FastApi(lifespan=lifespan)
    ```
    """
    def __init__(self,
                 db_url: str = DATA_BASE_URL,
                 poolclass: Pool | None = None,
                 ) -> None:
        """
        Args:
            db_url (str, optional): Адресс Базы Данных. Defaults to DATA_BASE_URL.

            poolclass (Pool | None, optional): Пул типа :class:`sqlalchemy.pool.Pool`.
            Defaults to None.
        """
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
        """
        Закрытие соединения
        """
        await self.engine.dispose()

    def get_scoped_session(self) -> AsyncSession:
        """
        Получение сессии
        """
        session = async_scoped_session(
            session_factory=self.session,
            scopefunc=current_task,
        )
        return session

    async def session_geter(self) -> AsyncGenerator[AsyncSession, Any]:
        """
        Получение генератора сессии

        Returns:
            AsyncGenerator[AsyncSession, Any]: Возвращает
            генератор с сессиями

        Yields:
            Iterator[AsyncGenerator[AsyncSession, Any]]: Генератор подает
            сессии
        """
        session = self.get_scoped_session()
        yield session
        await session.remove()


db_helper = DataBaseHelper()
db_test = DataBaseHelper
