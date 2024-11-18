from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from starlette.config import Config


base_dir = Path(__file__).resolve().parent.parent.parent
log_dir = base_dir.joinpath('logs')


config = Config('.env')


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
    rabbit: RabbitSettings = RabbitSettings()
    debug: bool = bool(int(config('DEBUG')))
    API_PREFIX: str = '/api/v1'
    BASE_DIR: Path = base_dir
    LOG_DIR: Path = log_dir


settings = Settings()
