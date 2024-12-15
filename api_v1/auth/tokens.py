from fastapi_users.authentication.strategy import JWTStrategy
from fastapi_users.jwt import generate_jwt


class JWTStrategyWithEmail(JWTStrategy):
    """
    JWT стратегия с дополнительными полями
    """

    async def write_token(self, user):
        data = {"sub": str(user.id),
                "aud": self.token_audience,
                "email": str(user.email)}
        return generate_jwt(
            data,
            self.encode_key,
            self.lifetime_seconds,
            algorithm=self.algorithm,
        )
