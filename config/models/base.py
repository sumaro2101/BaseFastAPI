from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            declared_attr,
                            )


class Base(DeclarativeBase):
    """
    Базовая модель для инициализации других моделей.

    Данная базовая модель является абстактной, и определяет
    базовое поведение других таблиц.

    ## Определение поведения таблиц:

    - Имя любой таблицы приводится к :method:`lower()` и
    добаляется `s` к окончанию.

    - Для каждой таблицы создается автогенерируемое поле `id` или `uid`,
    которое автоинкремирует счетчик интидификатора сущностей.
    
    ## Примеры:
    ```python
    from sqlalchemy.orm import Mapped, mapped_column
    from sqlalchemy import String
    from sqlalchemy.types import LargeBinary
    from datetime import date

    from config.models import Base
    
    
    class User(Base):
        name: Mapped[str] = mapped_column(String(length=100))
        surname: Mapped[str] = mapped_column(String(length=200))
        password: Mapped[str] = mapped_column(LargeBinary)
        active: Mapped[bool] = mapped_column(default=True)
        is_admin: Mapped[bool] = mapped_column(default=False)
        create_date: Mapped[datetime] = mapped_column(
            insert_default=func.now(),
            server_default=func.now(),
            )
        login_date: Mapped[datetime | None] = mapped_column(
            default=None,
            server_default=None,
            nullable=True,
            )
    ```
    По итогу к классу :class:`User` будет добавленно поле `id` или `uid`,
    а так же в Базу данных таблица будет с названием `users`.
    """
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    id: Mapped[int] = mapped_column(primary_key=True)
