# Title
Данный проект является большим онлайн магазином. (Стадия разработки)

# TO DO
## Stripe
Проект реализует интеграцию с внешним API платежной системы Stripe.
Реализованны Классы для интеграции:
- Stripe # Абстрактный класс определяющий каркасс
- CreateStripeItem # Создание Stripe объекта
- UpdateStripeItem # Обновление Stripe объекта
- ActivateStipeItem # Активация Stripe объекта
- DeactivateStripeItem # Деактивация Stripe объекта
- StripeItems # Список Stripe объектов
- CreateDiscountCoupon # Создание скидочного купона
- UpdateDiscountCoupon # Обновление скидочного купона
- DeleteDiscountCoupon # Удаление скидочного купона
- StripeSession # Создание Stripe Сессии для оплаты
- ExpireSession # Отмена Stripe Cессии

Создание Stripe объекта
```python
values = dict(
    id=1,
    name='Stripe',
    price=50000,
)
stripe = CreateStripeItem(values)
await stripe.action()
```

Обновление Stripe объекта
```python
values = dict(
    id=1,
    name='Updated_Stripe',
)
stripe = UpdateStripeItem(values)
await stripe.action()
```

Деактивация Stripe объекта
```python
values = dict(
    id=1,
)
stripe = DeactivateStripeItem(values)
await stripe.action()
```

Активация Stripe объекта
```python
values = dict(
    id=1,
)
stripe = ActivateStipeItem(values)
await stripe.action()
```

Список Stripe объектов
```python
list_items = [
    <Product1>,
    <Product2>,
    <Product3>,
    ]
stripe = StripeItems(
    products=list_items,
    add_key=True,
)
# add_key необходим в случае ручного использования,
# для того что бы система автоматически добавила API_KEY
# к запросу Stripe
```

Создание скидочного купона
```python
values = dict(
    id=1,
    number='COUPON',
    discount=22.0,
    end_at=8043214523, # UNIX-time required
)
stripe = CreateDiscountCoupon(values)
await stripe.action()
```

Обновление скидочного купона
```python
values = dict(
    id=1,
    number='NEWCOUPON',
)
stripe = UpdateDiscountCoupon(values)
await stripe.action()
```

Удаление скидочного купона
```python
values = dict(
    id=1,
)
stripe = DeleteDiscountCoupon(values)
await stripe.action()
```

Создание Сессии для платежа
```python
user = <User1>
list_items = [
    <Product1>,
    <Product2>,
    <Product3>,
    ]
unique_code = int_to_base36(getrandbits(41))
promo = 1
session = StripeSession(
    user=user,
    products=list_items,
    unique_code=unique_code,
    promo=promo,
)
session.get_session_payments()
# unique_code неоходим для защиты сессии от злоумышленного
# использования. Этот код идентифицирует текущую корзину.
# При совершении покупки и создании заказа этот код удаляется из текущей корзины,
# по этому создать дополнительные заказы просто посредством перехода на ту же ссылку
# не возможно.
```

Отмена Stripe Сессии
```python
basket = <Basket1>
ExpireSession(
    session_id=basket.session_id,
).expire_session()
```

## RabbitMQ, Celery
Используется Брокер сообщений RabbitMQ и Worker Celery
### Docker RabbitMQ
```yaml
rabbitmq:
    hostname: rabbitmq
    image: rabbitmq:4.0.3-management
    env_file:
      - .env
    ports:
      - 5672:5672
      - 15672:15672
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq

volumes:
  rabbitmq-data:
```

### Настройка RabbitMQ
```python
# .env
RABBITMQ_DEFAULT_USER=guest # Логин RabbitMQ
RABBITMQ_DEFAULT_PASS=guest # Пароль RabbitMQ
```

### Docker Celery Worker
```yaml
celery_worker:
    build: 
      context: .
      dockerfile: ./docker/fastapi/Dockerfile
    command: /start-celeryworker
    volumes:
      - .:/app
    env_file:
      - .env
```

### Настройка Celery
```python
# congin/rabbitmq/connection.py
from config.config import settings


app = Celery(__name__)
app.conf.broker_url = settings.rabbit.broker_url
app.autodiscover_tasks(packages=['project.packages'])
```

### Класс Celery
Есть реализация Асихронного класса Celery
для выполнения задач в асинхронном режиме.

### Использование
После настройки RabbitMQ и Celery
Вам необходимо запустить проект (инструкции ниже)
а затем перейти по адрессу:
http://localhost:15672/
Это будет страница RabbitMQ для просмотра всех каналов, очередей,
обмеников, пользователей, и.т.д.
Вам нужно будет ввести логин и пароль для аутентификации который вы указали в .env

## Flower
Flower это мощное приложение для отслеживания всех
задач на стороне Worker.
### Docker Flower
```yaml
dashboard:
    build: 
      context: .
      dockerfile: ./docker/fastapi/Dockerfile
    command: /start-flower
    volumes:
      - .:/app
    ports:
      - 5555:5555
    env_file:
      - .env
```

### Настройка
Предварительная настройка не требуется, все настройки подтягиваются
автоматически из RabbitMQ.

### Использование
Для использования Flower вам нужно перейти по адрессу:
http://localhost:5555/
У вас откроется страница Flower с полной информацией о Worker и Tasks.

# Dependencies
В проекте используются зависимости:
- fastapi
- pydantic
- pydantic-settings
- sqlalchemy
- asyncpg
- psycopg2-binary
- alembic
- pyjwt
- bcrypt
- python-multipart
- stripe
- pytz
- uvicorn
- python-dotenv
- celery
- flower

## SQLAlchemy
SQLAlchemy используется асинхронный.
Реализованн специальный класс для поддежки подключения и 
делегированнием сессий.
- DataBaseHelper

```python
# Инициализация соединения с Базой Данных на текущий HTTP запрос
async with db_helper.engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
    yield # Событие HTTP запроса
await db_helper.dispose()

# "Протаскивание" текущей сессии для запросов к Базе данных на этот HTTP запрос
async def get_session(session: AsyncSession = Depends(db_helper.session_geter)):
    current_session = session
    return session
```

# Install
## ENV
Для запуска проекта вам нужно установить переменные окружения
```python
# .env
POSTGRES_PASSWORD=password # Пароль базы данных (настройка)
DB_PASSWORD=password # Пароль базы даных (использование)
RABBITMQ_DEFAULT_USER=user # Логин для RabbitMQ
RABBITMQ_DEFAULT_PASS=password # Пароль для RabbitMQ
STRIPE_API=some_stripe:api # API_KEY stripe платежная система
```
Для получения API_KEY Stripe вам нужно перейти на официальную страницу Stripe [link](https://stripe.com)
и зарегистрироваться, в последствии вы получите ключи для API.

## Certifications
- Перейдите в папку сертификатов
```bash
cd certs
```

- Создание приватного ключа
```bash
openssl genrsa -out jwt-private.pem 2048
```

- Создание публичного ключа на основе приватного
```bash
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

## Docker
Проект находится под системой контеризации Docker
Если у вас нет Docker, прейдите на официальную страницу Docker [link](https://www.docker.com)
и скачайте от туда Docker (в случае если у вас система MAC, Windows, в ином установка посредством терминала).

Неоходимо совершить билд образов и контейнеров
```bash
docker compose build
```
Затем запустить образы
```bash
docker compose up
```

# OpenAI
FastAPI поддерживает автоматическую генерацию документации и взаимодействие с API.
Для более легкого просмотра возможностей проекта (пока нет клиента) вы можете прейти по ссылке:
http://localhost:8080/docs/
