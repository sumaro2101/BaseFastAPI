from config import celery_app
import asyncio


@celery_app.task
async def time_sleep_task():
    """
    Тестовая задача для Celery
    """
    await asyncio.sleep(2.0)
    return 'Task is done'
