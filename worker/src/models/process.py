from broker.broker import RabbitMq
from core.config import settings
from db.clickhouse import Clickhouse


class Process:
    async def __aenter__(self):
        self.broker = RabbitMq(
            host=settings.rabbitmq.host,
            port=settings.rabbitmq.port,
            username=settings.rabbitmq.username,
            password=settings.rabbitmq.password,
        )
        self.storage = Clickhouse(
            host=settings.clickhouse.host,
            port=settings.clickhouse.port,
            user=settings.clickhouse.user,
            password=settings.clickhouse.password,
        )
        await self.broker.connect()
        await self.storage.connect()
        await self.storage.create_table()
        self.status = None
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.broker.connection:
            await self.broker.connection.close()
        if self.storage.cursor:
            await self.storage.cursor.close()
        if self.storage.connection:
            await self.storage.connection.close()

    async def read_queue(self, queues):
        for queue in queues:
            await self.broker.consumer(queue)
            if self.broker.message:
                return True

    async def check_status(self, response):
        if not response:
            self.status = "ok"
        else:
            self.status = "error"
