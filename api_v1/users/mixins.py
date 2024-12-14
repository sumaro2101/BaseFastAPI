from fastapi import status
from loguru import logger

from .exceptions import PasswordNotValidError


class ActionUserManagerMixin:
    """
    Миксин для поддержки методов UserManager которые отвечают
    за дополнительную логику
    """
    async def on_after_request_verify(self, user, token, request):
        """
        Здесь должна быть отправка на E-mail `token` который уже
        вмещает в себя дополнительное поле `email` для верификации.
        Этот токен нужно вписать в end-point `verify`.

        Для эмуляции отправки сюда в консоль выведется сам токен.

        Если в консоли вы не видете токена значит:
        - Вы уже верифицированы
        - Не правильные данные
        - Не активный пользователь

        Args:
            user (_type_): пользователь
            token (_type_): Токен с email
            request (_type_): сущность request
        """
        logger.warning('TOKEN VERIFY ^^^^^------^^^^^ TOKEN VERIFY\n')
        logger.warning(token)
        logger.warning('\nEND TOKEN ^^^^^------^^^^^ END TOKEN')

    async def on_after_forgot_password(self, user, token, request):
        """
        Здесь должна быть отправка на E-mail `token` который уже
        вмещает в себя дополнительное поле `password_fgpt` для верификации.
        Этот токен нужно вписать в end-point `reset-password`.

        Для эмуляции отправки сюда в консоль выведется сам токен.

        Если в консоли вы не видете токена значит:
        - Не правильные данные
        - Не активный пользователь

        Args:
            user (_type_): пользователь
            token (_type_): Токен с password_fgpt
            request (_type_): сущность request
        """
        logger.warning('TOKEN RESET ^^^^^------^^^^^ TOKEN RESET\n')
        logger.warning(token)
        logger.warning('\nEND TOKEN ^^^^^------^^^^^ END TOKEN')

    async def on_after_reset_password(self, user, request):
        """
        Здесь должна быть отправка на E-mail cообщения о изменения пароля.

        Args:
            user (_type_): пользователь
            request (_type_): сущность request
        """
        return await super().on_after_reset_password(user, request)


class PasswordValidationMixin:
    """
    Миксин добавляющий валидацию пароля
    """

    async def validate_password(self, password, user):
        if not len(password) > 7:
            raise PasswordNotValidError(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password is to short',
                )
