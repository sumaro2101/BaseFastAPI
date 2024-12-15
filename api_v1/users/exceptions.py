from fastapi_users.exceptions import FastAPIUsersException
from starlette.exceptions import HTTPException


class PasswordNotValidError(HTTPException):
    """
    Исключение не валидного пароля
    """

    pass


class UserNotVerified(FastAPIUsersException):
    """
    Исключение не верифицинованного пользователя
    """

    pass
