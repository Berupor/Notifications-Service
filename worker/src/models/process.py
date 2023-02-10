from broker.broker import RabbitMq


class Process:
    async def __aenter__(self):
        self.broker = RabbitMq()
        self.broker.connection = await self.broker.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.broker.close()

    async def read_queue(self, queues):
        for queue in queues:
            await self.broker.consumer(queue)
            if self.broker.message:
                return True
