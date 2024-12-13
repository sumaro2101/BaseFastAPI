import jwt
from fastapi_users.jwt import decode_jwt
from fastapi_users import exceptions

from .exceptions import UserNotVerified, PasswordNotValidError


class AuthenticationUserManagerMixin:
    """
    Миксин добавляющий аутентификацию в логику менеджера
    """

    async def authenticate_user(self, token: str | None):
        if not token:
            return
        try:
            data = decode_jwt(
                token,
                self.verification_token_secret,
                [self.verification_token_audience],
            )
        except jwt.PyJWTError:
            raise exceptions.InvalidVerifyToken()

        try:
            user_id = data["sub"]
            email = data["email"]
        except KeyError:
            raise exceptions.InvalidVerifyToken()

        try:
            user = await self.get_by_email(email)
        except exceptions.UserNotExists:
            return

        try:
            parsed_id = self.parse_id(user_id)
        except exceptions.InvalidID:
            raise exceptions.InvalidVerifyToken()

        if parsed_id != user.id:
            raise exceptions.InvalidVerifyToken()

        if not user.is_verified:
            raise UserNotVerified()

        return user


class PasswordValidationMixin:
    """
    Миксин добавляющий валидацию пароля
    """

    async def validate_password(self, password, user):
        if not len(password) > 7:
            raise PasswordNotValidError('Password is not valid')
