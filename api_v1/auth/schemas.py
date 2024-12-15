from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """
    Схема пользователя
    При добавлении полей в модель, так же
    необходимо добавить поля - тут!
    """

    pass


class UserCreate(schemas.BaseUserCreate):
    """
    Схема создания пользователя
    При добавлении полей в модель, так же
    необходимо добавить поля - тут!
    """

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """
    Схема обновления пользователя
    При добавлении полей в модель, так же
    необходимо добавить поля - тут!
    """

    pass
