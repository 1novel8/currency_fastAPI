import asyncio
import json

from celery import Celery
from kafka import KafkaConsumer, KafkaProducer
from kombu import Exchange, Queue

from src.config import settings
from src.services import CurrencyService

app = Celery('celery')

app.config_from_object('src.config:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Minsk'
app.autodiscover_tasks()

app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('new_currencies', Exchange('new_currencies'), routing_key='new_currency'),
    Queue('update_currencies', Exchange('update_currencies'), routing_key='update_currencies'),
)

app.conf.beat_schedule = {
    'receive_new_currencies': {
        'task': 'src.celery_tasks.receive_new_currencies',
        'schedule': 30,
    },
    'update_currencies': {
        'task': 'src.celery_tasks.update_and_send_currencies',
        'schedule': 30,
    }
}


@app.task(queue='new_currencies')
def receive_new_currencies() -> None:
    """
    Task checks if new currencies appeared from django service
    """

    loop = asyncio.get_event_loop()

    async def do_async():
        consumer = KafkaConsumer(
            'new_currencies',
            bootstrap_servers=settings.KAFKA_URL,
            consumer_timeout_ms=5000,
        )
        service = CurrencyService()
        for message in consumer:
            name = message.value.decode('utf-8')
            await service.create(name=name)

    loop.run_until_complete(do_async())


@app.task(queue='update_currencies')
def update_and_send_currencies() -> None:
    """
    Updates all currencies in database and sends it to django service
    """

    loop = asyncio.get_event_loop()

    async def do_async():
        producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_URL,
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
        )

        service = CurrencyService()
        name_list = await service.list_of_names()
        for name in name_list:
            currency = await service.update(name=name)
            if currency:
                producer.send('update_currencies', value=currency.model_dump())
        producer.flush()

    loop.run_until_complete(do_async())
