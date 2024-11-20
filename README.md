# Title
Данный шаблон был разработан для одной цели - облегчения и повышения качества
выполненых тестовых заданий в рамках **FastAPI**.

# Quick start
Для тех кто уже знаком с реализацией и всеми деталями - могут приступить к установке.
## Enviroments
Необходимо заполнить **.env.sample** и в последствии перемеиновать его в **.env**
```python
# .env.sample
POSTGRES_PASSWORD=password # Пароль от базы данных (Настройка)
DB_PASSWORD=password # Пароль от базы данных (Использование)
TEST_POSTGRES_PASSWORD=password # Пароль от тестовой базы данный (Настройка)
TEST_DB_PASSWORD=password # Пароль от тестовой базы данных (Использование)
```
## Docker
Шаблон находится под системой управления и контеризации - **Docker**.
Если у вас нет Docker - вы можете установить его с официального сайта: [Docker](https://www.docker.com/get-started/)
- Вам необходимо сделать "Билд"
```bash
docker compose build
```
- Вам необходимо запустить окружение
```bash
docker compose up
```
- После успешного запуска приложение будет доступно по адрессу: http://localhost:8080

# View
Обзор и детали данного шаблона
## Найболее используемые
Найболее используемые конструкции с которыми приходится часто взаимодействовать.
- registration routers
    - В каждом приложений необходимо инициализировать router
    ```python
    # api/users/views.py
    from fastapi import APIRouter


    router = APIRouter(prefix='/users',
                    tags=['Users'],
                    )
    ```
    - Затем зарегистрировать роутер
    ```python
    # api_v1/routers.py
    from api_v1.users.views import router as users


    # В этой функции нужно по порядку регистрировать routers
    def register_routers(app: FastAPI) -> None:
    app.include_router(
        router=users,
        prefix=settings.API_PREFIX,
    )
    ```
    После регистрации данные маршруты будут доступны.
- registration logs
    - Логи захватывают все исключения возникшие в системе
    и с помошью дисперичизации распределяется по нужным **file.log**
    ```python
    # app_includes/logs_errors.py
    from fastapi import FastAPI
    from api_v1.exeptions import ValidationError


    # В данной функции регистрируются все исключения для захватывания Логами
    def register_errors(app: FastAPI) -> None:
        @app.exception_handler(ValidationError)
        async def validation_error_handler(
            request: Request,
            exc: ValidationError,
        ):
            logger.opt(exception=True).warning(exc)
            response = dict(
                status=False,
                error_code=exc.status_code,
                message=exc.detail,
            )
            return JSONResponse(response)
    ```
    - Если вы пишете пользовательское исключение например:
    ```python
    from starlette.exceptions import HTTPException


    class ValidationError(HTTPException):

    pass
    ```
    То вам нужно его зарегистрировать как было показанно выше,
    иначе logs не смогут выявить данное исключение и данные будут потеряны.
- registration middlaware