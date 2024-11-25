FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_V=1.8.3
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app

RUN adduser user \
    && addgroup docker \
    && adduser user docker

RUN pip install poetry

COPY pyproject.toml ./

RUN poetry install --no-root

RUN apt-get update \
    && pip install --upgrade pip \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev \
    && apt-get install -y gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


COPY ./docker/fastapi/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/fastapi/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./docker/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./docker/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./docker/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

WORKDIR /app

RUN chown -R user:user .

USER user