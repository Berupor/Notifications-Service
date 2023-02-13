import aiormq

from core.config import settings


class RabbitMQBroker:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aiormq.connect(
            f"amqp://{self.username}:{self.password}@{self.host}//"
        )
        self.channel = await self.connection.channel()

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def produce(self, message: str, queue_name: str):
        await self.channel.queue_declare(queue_name, auto_delete=True)

        await self.channel.basic_publish(message.encode(), routing_key=queue_name)


rabbitmq_broker: RabbitMQBroker = RabbitMQBroker(
    host=settings.rabbitmq.host,
    port=settings.rabbitmq.port,
    username=settings.rabbitmq.username,
    password=settings.rabbitmq.password,
)


def get_rabbitmq() -> RabbitMQBroker:
    """Function required for dependency injection"""
    return rabbitmq_broker
