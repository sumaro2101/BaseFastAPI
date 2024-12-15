from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer

from config.models.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель пользователя
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
