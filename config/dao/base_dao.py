from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Select
from sqlalchemy.orm import joinedload, selectinload
from typing import ClassVar, Sequence

from config import BaseModel


class BaseDAO:
    """
    Базовый DAO класс для CRUD модели

    Универсальный класс для легкого опеределения

    CRUD модели

    Примеры::

        # Поиск сущности
        item = ModelDAO.find_item_by_args(
            session=session,
            id=3,
        )
        # Множественный поиск сущностей
        items = ModelDAO.find_all_items_by_args(
            session = session,
            one_to_many = (Model.tag,),
            name='model',
        )
        # Создание сущности
        item = ModelDAO.add(
            session,
            id=3,
            name='model',
            )
    """
    model: ClassVar[BaseModel | None] = None

    @classmethod
    async def find_item_by_args(cls,
                                session: AsyncSession,
                                one_to_many: Sequence[BaseModel] | None = None,
                                many_to_many: Sequence[BaseModel] | None = None,
                                **kwargs: dict[str, str | int],
                                ) -> BaseModel:
        """
        Нахождение и возращение сущности

        Args:
            session (AsyncSession): Текущая сессия

            one_to_many (Sequence[BaseModel] | None, optional): Выбранные поля 
                для one_to_many
                которые имеют отношение например: (Product.user)

            many_to_many (Sequence[BaseModel] | None, optional): Выбранные поля 
                для many_to_many
                которые имеют отношение например: (Product.categories)

        Returns:
            BaseModel: Сущность из выборки
        """
        stmt = struct_options_statment(
            model=cls.model,
            one_to_many=one_to_many,
            many_to_many=many_to_many,
            **kwargs,
        )
        result = await session.scalar(statement=stmt)
        return result

    @classmethod
    async def find_all_items_by_args(cls,
                                     session: AsyncSession,
                                     one_to_many: Sequence[BaseModel] | None = None,
                                     many_to_many: Sequence[BaseModel] | None = None,
                                     **kwargs: dict[str, str | int],
                                     ) -> list[BaseModel]:
        """
        Нахождение и возращение множества сущностей

        Args:
            session (AsyncSession): Текущая сессия

            one_to_many (Sequence[BaseModel] | None, optional): Выбранные поля 
                для one_to_many
                которые имеют отношение например: (Product.user)

            many_to_many (Sequence[BaseModel] | None, optional): Выбранные поля 
                для many_to_many
                которые имеют отношение например: (Product.categories)

        Returns:
            BaseModel: Сущности из выборки
        """
        stmt = struct_options_statment(
            model=cls.model,
            one_to_many=one_to_many,
            many_to_many=many_to_many,
            **kwargs,
        )
        result = await session.scalars(statement=stmt)
        return list(result)

    @classmethod
    async def add(cls,
                  session: AsyncSession,
                  **values,
                  ) -> BaseModel:
        async with session.begin():
            instance = cls.model(**values)
            session.add(instance=instance)
            try:
                await session.commit()
            except SQLAlchemyError as ex:
                await session.rollback()
                raise ex
            return instance


def struct_options_statment(model: BaseModel,
                            one_to_many: Sequence[BaseModel] | None = None,
                            many_to_many: Sequence[BaseModel] | None = None,
                            **kwargs: dict[str, str | int],
                            ) -> Select:
    """
    Струкрутирование запроса SELECT для выборки

    Args:
        model (BaseModel): Модель таблицы для выборки
        one_to_many (Sequence[BaseModel] | None, optional): Выбранные поля 
            для one_to_many
            которые имеют отношение например: (Product.user)

        many_to_many (Sequence[BaseModel] | None, optional): Выбранные поля 
            для many_to_many
            которые имеют отношение например: (Product.categories)

    Returns:
        Select: Экземпляр запроса
    """
    if one_to_many and many_to_many:
        stmt = (Select(model)
                .filter_by(**kwargs)
                .options(joinedload(*one_to_many))
                .options(selectinload(*many_to_many)))
    elif one_to_many:
        stmt = (Select(model)
                .filter_by(**kwargs)
                .options(joinedload(*one_to_many)))
    elif many_to_many:
        stmt = (Select(model)
                .filter_by(**kwargs)
                .options(selectinload(*many_to_many)))
    else:
        stmt = (Select(model)
                .filter_by(**kwargs))
    return stmt
