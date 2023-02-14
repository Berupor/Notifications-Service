from functional.src.utils.mock_data import mock_notification, mock_user


class MockUserService:
    async def find_one(self, **kwargs):
        return mock_user


class MockNotificationsService:
    async def find_one(self, **kwargs):
        return mock_notification


class MockRabbitMQBroker:
    def __init__(self, host, port, username, password):
        ...

    async def produce(self, message: str, queue_name: str):
        return None
