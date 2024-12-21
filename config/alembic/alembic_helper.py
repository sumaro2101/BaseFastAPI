from pathlib import Path
from alembic.command import upgrade
from alembic.config import Config
from typing import ClassVar
from sqlalchemy.ext.asyncio.engine import AsyncConnection


from config import settings


class AlembicHelper:
    """
    Вспомогательный класс для Alembic
    """
    config: ClassVar[Config] = Config
    migration_path: ClassVar[Path] = settings.alembic.MIGRATION_PATH

    def __init__(self,
                 sql_url: str | Path,
                 ):
        self.sql_url = sql_url

    def get_config(self, connection: AsyncConnection) -> Config:
        cfg = self.config()
        cfg.set_main_option('sqlalchemy.url',
                            self.sql_url)
        cfg.set_main_option('script_location',
                            self.migration_path.as_posix())
        cfg.attributes['connection'] = connection
        return cfg

    def make_upgrade(self, connection: AsyncConnection):
        config = self.get_config(connection=connection)
        upgrade(config, 'head')
