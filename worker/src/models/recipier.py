from core.config import settings
from models.recipients.email import Email


class Recipier:
    def __init__(self, type: str):
        self.type = type
        self.service = None
        if self.type == "email":
            self.service = Email(
                host=settings.email_server.host, port=settings.email_server.port
            )

    async def __aenter__(self):
        await self.service.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.service.close_connect()
