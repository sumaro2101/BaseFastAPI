from fastapi import FastAPI

from config import settings
from api_v1.users.views import router as users


def register_routers(app: FastAPI) -> None:
    """
    Функция по регистрации роутеров

    ## Args:
        app (FastAPI): ASGI приложение.

    ## Returns:
        None
    
    ## Example
    ```python
    from fastapi import FastAPI

    from config import settings
    from api_v1.api_xml.views import router as xml
    from api_v1.users.views import router as users


    def register_routers(app: FastAPI) -> None:
        app.include_router(
        router=xml,
        prefix=settings.API_PREFIX,
        )
        # Новый роутер
        app.include_router(
        router=users,
        prefix=settings.API_PREFIX,
        )
    ```
    """
    app.include_router(
        router=users,
        prefix=settings.API_PREFIX,
        )
