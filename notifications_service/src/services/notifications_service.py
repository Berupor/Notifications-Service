from db.models.models import Notification
from sqlalchemy.future import select
from services.base_postgres_service import BaseService


class NotificationsService(BaseService):
    _model = Notification

    async def find_one(self, **kwargs):
        async with self._session() as session:
            query = select(self._model).filter_by(**kwargs)

            notification = await session.execute(query)
            return notification.scalar()


notification_service: NotificationsService = NotificationsService()


def get_notification_service() -> NotificationsService:
    """Function for dependency injection"""

    return notification_service
