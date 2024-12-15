# Title

Данный шаблон был разработан для одной цели - облегчения и повышения качества
выполненых тестовых заданий в рамках **FastAPI**.

# Quick start

Для тех кто уже знаком с реализацией и всеми деталями - могут приступить к установке.

## GIT

Для безопасного выполнения копирования из GitHub Необходимо сделать следующее:

- Клонировать Git репозиторий

```bash
git clone https://github.com/sumaro2101/BaseFastAPI your_name_dir
```

Где <https://github.com/sumaro2101/BaseFastAPI> - адресс репозитория,
`your_name_dir` - имя папки для клонирования

- Удалить .git из клонированного репозитория

```bash
rm -r .git
```

или если отказывает в доступе можете - переместить

```bash
mv .git ../git
```

- Инициализировать свой `Git`

```bash
git init
```

- Сделать свой коммит

```bash
git add .
git commit -m 'base commit'
```

- Привязать текущий Git к вашему удаленному репозиторию

```bash
git remove add origin some_url_or_ssh_repo
```

- Отправить на удаленный репозиторий текущий репозиторий

```bash
git push -u origin main
```

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

- После успешного запуска приложение будет доступно по адрессу: <http://localhost:8080>
- Grafana: <http://localhost:3000>
- Flower: <http://localhost:5555>

# View

Обзор и детали данного шаблона

## Users

В данном шаблоне реализован CRUD для пользователя с помощью библиотеки
[fastapi-users](https://fastapi-users.github.io/fastapi-users/latest/)

### End-points

`USERS`

- <http://localhost:8080/api/v1/users/me> GET
Получение текущего пользователя
- <http://localhost:8080/api/v1/users/me> PATCH
Изменение текущего пользователя
- <http://localhost:8080/api/v1/users/{id}> GET
Получение пользователя по ID Необходимо иметь права доступа уровня `admin`
- <http://localhost:8080/api/v1/users/{id}> PATCH
Изменение пользоватея по ID Необходимо иметь права доступа уровня `admin`
- <http://localhost:8080/api/v1/users/{id}> DELETE
Удаление пользоватея по ID Необходимо иметь права доступа уровня `admin`

`AUTH`

- <http://localhost:8080/api/v1/auth/jwt/login> POST
Аутентификация в систему с последующим получением JWT для авторизации
- <http://localhost:8080/api/v1/auth/jwt/logout> POST
Вызод из системы
- <http://localhost:8080/api/v1/auth/register> POST
Регистрация нового пользователя
- <http://localhost:8080/api/v1/auth/request-verify-token> POST
Получение токена для верификации. `ВАЖНО` Читайте ниже, есть нюанс.
- <http://localhost:8080/api/v1/auth/verify> POST
Верификация пользователя по токену
- <http://localhost:8080/api/v1/auth/forgot-password> POST
Получение токена для изменения пароль. `ВАЖНО` Читайте ниже, есть нюанс.
- <http://localhost:8080/api/v1/auth/reset-password> POST
Изменения пароля посредством токена

`ВАЖНО`

- <http://localhost:8080/api/v1/auth/forgot-password> POST
Должен осуществлять логику отправки токена по эмеилу либо другим способом.
В данный момент отправка осуществляется через `консоль`.
Для деталей смотрите миксин `api_v1/users/mixins/ActionUserManagerMixin`
- <http://localhost:8080/api/v1/auth/forgot-password> POST
Должен осуществлять логику отправки токена по эмеилу либо другим способом.
В данный момент отправка осуществляется через `консоль`.
Для деталей смотрите миксин `api_v1/users/mixins/ActionUserManagerMixin`

### Transport

В fastapi-users есть 2 вида транспорта:

- [Bearer](https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/transports/bearer/)
- [Cookie](https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/transports/cookie/)

В шаблоне реализован Bearer способ:

```python
from fastapi_users.authentication import BearerTransport

from config import settings


bearer_transport = BearerTransport(settings.CURRENT_ORIGIN +
                                   settings.API_PREFIX +
                                   settings.JWT.JWT_PATH +
                                   '/login')
```

### Strategy

В fastapi-users есть 3 вида стратегии:

- [Database](https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/strategies/database/)
- [JWT](https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/strategies/jwt/)
- [Redis](https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/strategies/redis/)

В Шаблоне реализован JWT способ:

```python
from fastapi_users.authentication import JWTStrategy

from config import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.JWT.SECRET,
        lifetime_seconds=settings.JWT.RESET_LIFESPAN_TOKEN_SECONDS,
        )
```

## Найболее используемые

Найболее используемые конструкции с которыми приходится часто взаимодействовать.

### Registration Routers

- В каждом приложений необходимо инициализировать router

```python
# api/users/views.py
from fastapi import APIRouter


router = APIRouter(
    prefix='/users',
    tags=['Users'],
    )
```

- Затем зарегистрировать роутер

```python
# api_v1/routers.py
from api_v1.users.views import router as users
from config import settings


# В этой функции нужно по порядку регистрировать routers
def register_routers(app: FastAPI) -> None:
    app.include_router(
        router=users,
        prefix=settings.API_PREFIX,
    )
```

После регистрации данные маршруты будут доступны.

### Registration Logs

- Логи захватывают все исключения возникшие в системе
и с помошью диспечиризации распределяется по нужным **file.log**

```python
# app_includes/logs_errors.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse

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
иначе logs не смогут выявить данное исключение и данные будут утеряны.

### Registration Middlaware

- Для регистрации Middlaware вам нужно добавить его в функцию

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from config import settings


# Данная функция регистрирует все middleware
def register_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            settings.CURRENT_ORIGIN,
        ],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
```

- При появлении новых middleware добавляйте их по порядку в эту функцию

### Celery

- Для регистрации task вам нужно создать файл с именем **tasks.py** в вашем приложении:

```python
# api_v1/users/tasks.py
from config import celery_app
import asyncio


@celery_app.task
async def time_sleep_task():
    """
    Тестовая задача для Celery
    """
    await asyncio.sleep(2.0)
    return 'Task is done'
```

- Затем добавить этот файл в список пакетов Celery

```python
# confin.celery.connection.py

app = Celery(__name__)
app.conf.broker_url = settings.rabbit.broker_url
# Регистрация до окружения где находится tasks.py
app.autodiscover_tasks(packages=['api_v1.users'])
```

- После этих действий ваша task будет зарегистрирована

### Test

- Для тестирования у вас есть тестовая база данных, а так же
уже инициализированный отдельный клиент.
Cпособ реализации в **api_v1/tests/conftest.py**
- Что бы написать тестовую функцию которой нужен доступ к API,
вам нужно использовать fixture - client.

> [!NOTE]
> Для асинхронных тестов используйте **@pytest.mark.asyncio**

```python
# api_v1.tests.test_users.py
import pytest


@pytest.mark.asyncio
async def test_get_user_error(client: AsyncClient):
    response = await client.get(
        '/users/get',
    )
    assert response.status_code == 400
```

- Для запуска используйте команду

```bash
pytest
```
