import aiormq
from core.config import settings


async def on_message(message: aiormq.abc.DeliveredMessage):
    print(f" [x] Received message {message!r}")
    print(f"     Message body is: {message.body!r}")
    return message


class RabbitMq:
    def __init__(self):
        self.host = settings.rabbitmq.host
        self.port = settings.rabbitmq.port
        self.username = settings.rabbitmq.username
        self.password = settings.rabbitmq.password
        self.connection = None
        self.channel = None
        self.message = None

    async def connect(self):
        self.connection = await aiormq.connect(
            f"amqp://{self.username}:{self.password}@{self.host}//"
        )
        self.channel = await self.connection.channel()

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def save_message(self, message: aiormq.abc.DeliveredMessage):
        self.message = message
        return self

    async def consumer(self, queue: str):
        # параметр указывает на то, что воркер получит 1 сообщение
        # другими словами пока он не обработает сообщение, новое не возьмёт.
        await self.channel.basic_qos(prefetch_count=1)

        # объявление очереди
        declare_ok = await self.channel.queue_declare(
            queue, durable=False, auto_delete=True
        )

        # слушает очередь
        await self.channel.basic_consume(
            declare_ok.queue, self.save_message, no_ack=True
        )
