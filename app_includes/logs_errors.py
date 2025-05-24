from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi_users.exceptions import (
    InvalidID,
    UserAlreadyExists,
    UserNotExists,
    UserInactive,
    UserAlreadyVerified,
    InvalidVerifyToken,
    InvalidResetPasswordToken,
    InvalidPasswordException,
)

from http import HTTPStatus

from config.setup_logs.logging import logger
from api_v1.exeptions import ValidationError
from api_v1.users.exceptions import PasswordNotValidError


def register_errors(app: FastAPI) -> None:
    """
    Крючек для логирования различных исключений

    ## Args:
    app (FastAPI): ASGI приложение.

    ## Returns:
        None

    ## Example
    ```python
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    from fastapi.exceptions import HTTPException
    from http import HTTPStatus

    from config.setup_logs.logging import logger
    from api_v1.api_xml.exeptions import APIFileNotFoundError


    def register_errors(app: FastAPI) -> None:
            @app.exception_handler(HTTPException)
            async def http_error_handler(
                request: Request,
                exc: HTTPException,
            ):
                logger.opt(exception=True).warning(exc)
                response = dict(
                    status=False,
                    error_code=exc.status_code,
                    message=exc.detail,
                )
                return JSONResponse(response)

            # Добавление нового крюка
            @app.exception_handler(APIFileNotFoundError)
            async def file_not_found_error_handler(
                request: Request,
                exc: APIFileNotFoundError,
            ):
                logger.opt(exception=True).warning(exc)
                response = dict(
                    status=False,
                    error_code=exc.status_code,
                    message=exc.detail,
                )
                return JSONResponse(response)
    ```
    """

    @app.exception_handler(InvalidPasswordException)
    async def password_invalid_error_handler(
        request: Request,
        exc: InvalidPasswordException,
    ):
        """
        Логирование всех InvalidPasswordException
        """
        logger.opt(exception=True).warning(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        return JSONResponse(response, status_code=exc.status_code)

    @app.exception_handler(InvalidResetPasswordToken)
    async def password_token_error_handler(
        request: Request,
        exc: InvalidResetPasswordToken,
    ):
        """
        Логирование всех InvalidResetPasswordToken
        """
        logger.opt(exception=True).warning(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        return JSONResponse(response, status_code=exc.status_code)

    @app.exception_handler(InvalidVerifyToken)
    async def verify_token_error_handler(
        request: Request,
        exc: InvalidVerifyToken,
    ):
        """
        Логирование всех InvalidVerifyToken
        """
        logger.opt(exception=True).warning(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        return JSONResponse(response, status_code=exc.status_code)

    @app.exception_handler(UserAlreadyVerified)
    async def user_exists_error_handler(
        request: Request,
        exc: UserAlreadyVerified,
    ):
        """
        Логирование всех UserAlreadyVerified
        """
        logger.opt(exception=True).warning(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        return JSONResponse(response, status_code=exc.status_code)

    @app.exception_handler(UserInactive)
    async def user_activity_error_handler(
        request: Request,
        exc: UserInactive,
    ):
        """
        Логирование всех UserInactive
        """
        logger.opt(exception=True).warning(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        return JSONResponse(response, status_code=exc.status_code)

    @app.exception_handler(UserNotExists)
    async def user_not_exists_error_handler(
        request: Request,
        exc: UserNotExists,
    ):
        """
        Логирование всех UserNotExists
        """
        logger.opt(exception=True).warning(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        return JSONResponse(response, status_code=exc.status_code)

    @app.exception_handler(UserAlreadyExists)
    async def user_already_exists_error_handler(
        request: Request,
        exc: UserAlreadyExists,
    ):
        """
        Логирование всех UserAlreadyExists
        """
        logger.opt(exception=True).warning(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        return JSONResponse(response, status_code=exc.status_code)

    @app.exception_handler(InvalidID)
    async def invalid_id_error_handler(
        request: Request,
        exc: InvalidID,
    ):
        """
        Логирование всех InvalidID
        """
        logger.opt(exception=True).warning(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        return JSONResponse(response, status_code=exc.status_code)

    @app.exception_handler(PasswordNotValidError)
    async def password_validator_error_handler(
        request: Request,
        exc: PasswordNotValidError,
    ):
        """
        Логирование всех PasswordNotValidError
        """
        logger.opt(exception=True).warning(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        return JSONResponse(response, status_code=exc.status_code)

    @app.exception_handler(ValidationError)
    async def validation_error_handler(
        request: Request,
        exc: ValidationError,
    ):
        """
        Логирование всех ValidationError
        """
        logger.opt(exception=True).warning(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        return JSONResponse(response, status_code=exc.status_code)

    @app.exception_handler(HTTPException)
    async def http_error_handler(
        request: Request,
        exc: HTTPException,
    ):
        """
        Логирование всех HTTPException
        """
        logger.opt(exception=True).warning(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        return JSONResponse(response, status_code=exc.status_code)

    @app.exception_handler(Exception)
    async def error_handler(
        request: Request,
        exc: Exception,
    ):
        """
        Логирование всех Exception
        """
        logger.exception(exc)
        response = dict(
            status=False,
            error_code=500,
            message=HTTPStatus(500).phrase,
        )
        return JSONResponse(response, status_code=500)

    @app.exception_handler(StarletteHTTPException)
    async def validation_starlette_error_handler(
        request: Request,
        exc: StarletteHTTPException,
    ):
        """
        Логирование всех StarletteHTTPException
        """
        logger.opt(exception=True).warning(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        return JSONResponse(response, status_code=exc.status_code)
