import sys
from loguru import logger

from config import settings


log_dir = settings.LOG_DIR


def create_log_dirs() -> None:
    """
    Создание корневой папки для логов
    """    
    log_directory = settings.LOG_DIR
    log_directory.mkdir(parents=True, exist_ok=True)


logger.remove()

logger.add(
    log_dir.joinpath('access.log'),
    rotation='15MB',
    format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}',
    encoding='utf-8',
    enqueue=True,
    level='DEBUG',
    diagnose=False,
    backtrace=False,
    colorize=False,
    filter=lambda record: record['level'].no < 40,
)

logger.add(
    log_dir.joinpath('error.log'),
    rotation='15MB',
    format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}',
    encoding='utf-8',
    enqueue=True,
    level='ERROR',
    diagnose=False,
    backtrace=False,
    colorize=False,
)

logger.add(
    sink=sys.stderr,
    format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}',
    enqueue=True,
    level='ERROR',
    diagnose=False,
    backtrace=False,
    colorize=False,
)

logger.add(
    sink=sys.stdout,
    format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}',
    enqueue=True,
    level='DEBUG',
    diagnose=False,
    backtrace=False,
    colorize=False,
    filter=lambda record: record['level'].no < 40,
)
