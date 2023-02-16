from http import HTTPStatus

import asyncpg
import backoff
from fastapi import APIRouter, Depends

from api.v1.utls.decorators import exception_handler
from message_broker.rabbitmq.rabbitmq_broker import RabbitMQBroker, get_rabbitmq
from models.event import RequestEventModel, ResponseEventModel
from services.notifications_service import (
    NotificationsService,
    get_notification_service,
)
from services.user_service import UserService, get_user_service

router = APIRouter()

queue_priority = {1: "low", 2: "medium", 3: "high"}


@router.post(
    "/email/{user_id}",
    summary="Формирование данных для почтового уведомления.",
    description="Получение шаблона, почты пользователя и приведение данных к общему формату.",
    response_description="Статус обработки данных.",
)
@exception_handler
@backoff.on_exception(
    backoff.expo,
    (asyncpg.exceptions.PostgresWarning,),
    max_time=1000,
    max_tries=10,
)
async def email_notification(
    event: RequestEventModel,
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    notifications_service: NotificationsService = Depends(get_notification_service),
    message_service: RabbitMQBroker = Depends(get_rabbitmq),
) -> int:
    """Processing received event data.
    Args:
        event: Event data
        user_id: Id user
        user_service: Service for working with user
        notifications_service: Service for working with notifications
        message_service: Service for working with queue
    Returns:
        Execution status.
    """

    user = await user_service.find_one(id=user_id)
    notification = await notifications_service.find_one(name=event.notification_name)
    ready_data = ResponseEventModel(
        template=notification.template.html,
        user=user.to_dict(),
        data=notification.data,
        type="email",
    )

    await message_service.produce(
        ready_data.json(), queue_name=queue_priority[event.priority]
    )
    return HTTPStatus.ACCEPTED
