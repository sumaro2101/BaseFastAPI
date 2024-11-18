from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


def register_prometheus(app: FastAPI) -> None:
    """
    Регистрация Промитеуса
    """
    Instrumentator().instrument(app=app).expose(app=app)
