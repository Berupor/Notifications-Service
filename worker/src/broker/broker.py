from json import loads
import backoff

import aiormq


class RabbitMq:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None
        self.message = None

    @backoff.on_exception(
        backoff.expo,
        (
                ConnectionError
         ),
        max_time=1000,
        max_tries=10,
    )
    async def connect(self):
        self.connection = await aiormq.connect(
            f"amqp://{self.username}:{self.password}@{self.host}//"
        )
        self.channel = await self.connection.channel()

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def save_message(self, message: aiormq.abc.DeliveredMessage):
        self.message = loads(message.body.decode("utf-8"))
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
