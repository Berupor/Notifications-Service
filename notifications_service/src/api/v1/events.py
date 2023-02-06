from http import HTTPStatus

from fastapi import APIRouter, Depends

from message_broker.rabbitmq.rabbitmq_broker import (RabbitMQBroker,
                                                     get_rabbitmq)
from models.event import RequestEventModel, ResponseEventModel
from services.template_service import TemplateService, get_template_service
from services.user_service import UserService, get_user_service

router = APIRouter()

queue_priority = {1: "low", 2: "medium", 3: "high"}


@router.post(
    "/email/{user_id}",
    summary="Формирование данных для почтового уведомления.",
    description="Получение шаблона, почты пользователя и приведение данных к общему формату.",
    response_description="Статус обработки данных.",
)
async def email_notification(
        event: RequestEventModel,
        user_id: str,
        user_service: UserService = Depends(get_user_service),
        template_service: TemplateService = Depends(get_template_service),
        message_service: RabbitMQBroker = Depends(get_rabbitmq),
) -> int:
    """Processing received event data.
    Args:
        event: Event data
        user_id: Id user
        user_service: Service for working with user
        template_service: Service for working with templates
        message_service: Service for working with queue
    Returns:
        Execution status.
    """
    user = await user_service.find_one(id=user_id)
    template = await template_service.find_one(event_name=event.name)

    ready_data = ResponseEventModel(
        template=template.html,
        user=user.to_dict(), type="email"
    )

    await message_service.produce(
        ready_data.json(), queue_name=queue_priority[event.priority]
    )
    return HTTPStatus.ACCEPTED
