from fastapi_users.exceptions import FastAPIUsersException


class PasswordNotValidError(FastAPIUsersException):
    """
    Исключение не валидного пароля
    """

    pass


class UserNotVerified(FastAPIUsersException):
    """
    Исключение не верифицинованного пользователя
    """

    pass
