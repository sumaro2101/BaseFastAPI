from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

from http import HTTPStatus

from config.setup_logs.logging import logger
from api_v1.exeptions import ValidationError


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
        return JSONResponse(response)

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
        return JSONResponse(response)

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
        return JSONResponse(response)

    @app.exception_handler(StarletteHTTPException)
    async def validation_error_handler(
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
        return JSONResponse(response)
