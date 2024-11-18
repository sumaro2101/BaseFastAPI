import sys
from loguru import logger

from config import settings


log_directory = settings.LOG_DIR
log_directory.mkdir(parents=True, exist_ok=True)

logger.remove()

logger.add(
    log_directory.joinpath('access.log'),
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
    log_directory.joinpath('error.log'),
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
