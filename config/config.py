from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, ConfigDict
from starlette.config import Config
from celery.schedules import crontab


base_dir = Path(__file__).resolve().parent.parent
log_dir = base_dir.joinpath('logs')


config = Config('.env')


class JWTSettings(BaseModel):
    """
    Настройки JWT токена
    """
    NAME: str = 'jwt'
    SECRET: str = config('SECRET')
    RESET_LIFESPAN_TOKEN_SECONDS: int = 3600
    JWT_PATH: str = '/auth/jwt'


class AlembicSettings(BaseModel):
    """
    Настройки Alembic
    """
    CONFIG_PATH: Path = Path('alembic.ini')
    MIGRATION_PATH: Path = Path('async_alembic/')


class TestDBSettings(BaseModel):
    """
    Настройки тестовой базы данных
    """
    _engine: str = config('TEST_DB_ENGINE')
    _owner: str = config('TEST_DB_USER')
    _password: str = config('TEST_DB_PASSWORD')
    _name: str = config('TEST_DB_HOST')
    _db_name: str = config('TEST_DB_NAME')
    url: str = f'{_engine}://{_owner}:{_password}@{_name}/{_db_name}'


class DBSettings(BaseModel):
    """
    Настройки DataBase
    """
    _engine: str = config('DB_ENGINE')
    _owner: str = config('DB_USER')
    _password: str = config('DB_PASSWORD')
    _name: str = config('DB_HOST')
    _db_name: str = config('DB_NAME')
    url: str = f'{_engine}://{_owner}:{_password}@{_name}/{_db_name}'


class CelerySettings(BaseModel):
    """
    Настройки Celery
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    TIMEZONE: str = 'Europe/Moscow'
    TIMEDELTA_PER_DAY: crontab = crontab(minute=0,
                                         hour=2,
                                         day_of_week='*/1',
                                         day_of_month='*/1',
                                         month_of_year='*/1',
                                         )
    TEST_TIMEDELTA: crontab = crontab(minute='*/1')


class RabbitSettings(BaseModel):
    """
    Настройки RabbitMQ
    """
    RMQ_HOST: str = config('RMQ_HOST')
    RMQ_PORT: str = config('RMQ_PORT')
    RMQ_USER: str = config('RABBITMQ_DEFAULT_USER')
    RMQ_PASSWORD: str = config('RABBITMQ_DEFAULT_PASS')
    broker_url: str = ('amqp://' +
                       RMQ_USER +
                       ':' +
                       RMQ_PASSWORD +
                       '@' +
                       RMQ_HOST +
                       ':' +
                       RMQ_PORT)


class Settings(BaseSettings):
    """
    Настройки проекта
    """
    model_config = SettingsConfigDict(
        extra='ignore',
    )
    db: DBSettings = DBSettings()
    test_db: TestDBSettings = TestDBSettings()
    celery: CelerySettings = CelerySettings()
    rabbit: RabbitSettings = RabbitSettings()
    alembic: AlembicSettings = AlembicSettings()
    JWT: JWTSettings = JWTSettings()
    debug: bool = bool(int(config('DEBUG')))
    API_PREFIX: str = '/api/v1'
    BASE_DIR: Path = base_dir
    LOG_DIR: Path = log_dir
    CURRENT_ORIGIN: str = config('CURRENT_ORIGIN')


settings = Settings()
