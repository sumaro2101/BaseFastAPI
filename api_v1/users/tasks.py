from config import celery_app, settings
import asyncio


@celery_app.task
async def time_sleep_task():
    """
    Тестовая задача для Celery
    """
    await asyncio.sleep(2.0)
    return 'Task is done'


celery_app.conf.beat_schedule = {
    'test-every-10-seconds': {
        'task': 'llm_analizer.tasks.test',
        'schedule': settings.celery.TEST_TIMEDELTA,
        'args': ('hello',)
    },
}
