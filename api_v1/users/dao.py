from config.models import User
from config.dao import BaseDAO


class UserDAO(BaseDAO):
    """
    DAO для CRUD пользователя
    """
    model = User
