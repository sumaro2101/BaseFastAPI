from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from config import settings


def register_middlewares(app: FastAPI) -> None:
    """
    Регистрация middleware

    ## Args:
    app (FastAPI): ASGI приложение.

    ## Returns:
        None

    ## Example
    ```python
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi import FastAPI

    from config import settings
    from middlewares import SomeMiddleware


    def register_middlewares(app: FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[y
                settings.CURRENT_ORIGIN,
            ],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

        # Новая регистрация
        app.add_middleware(
            SomeMiddleware,
            *args,
        )
    ```
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            settings.CURRENT_ORIGIN,
        ],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
