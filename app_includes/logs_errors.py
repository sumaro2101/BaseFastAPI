import json
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

from http import HTTPStatus

from logs.logging import logger
from api_v1 import ValidationError


def register_errors(app: FastAPI) -> None:
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
            error_code=422,
            message=exc.detail,
        )
        json_response = json.dumps(response).encode(encoding='utf-8')
        return json_response

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
        json_response = json.dumps(response).encode(encoding='utf-8')
        return json_response

    @app.exception_handler(Exception)
    async def error_handler(
        request: Request,
        exc: Exception,
        ):
        """
        Логирование всех StarletteHTTPException
        """
        logger.exception(exc)
        response = dict(
            status=False,
            error_code=exc.status_code,
            message=exc.detail,
        )
        json_response = json.dumps(response).encode(encoding='utf-8')
        return json_response

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
            error_code=500,
            message=HTTPStatus(500).phrase,
        )
        json_response = json.dumps(response).encode(encoding='utf-8')
        return json_response
