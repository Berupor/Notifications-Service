from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from services.user_service import get_user_service, UserService
from message_broker.rabbitmq.rabbitmq_broker import get_rabbitmq, RabbitMQBroker

from models.event import RequestEventModel, ResponseEventModel

router = APIRouter()


@router.post(
    "email/{user_id}",
    summary="Формирование данных для почтового уведомления.",
    description="Получение шаблона, почты пользователя и приведение данных к общему формату.",
    response_description="Статус обработки данных.",
    response_model=ResponseEventModel,
)
async def email_notification(
        event: RequestEventModel,
        user_id: str,
        request: Request,
        user_service: UserService = Depends(get_user_service),
        message_service: RabbitMQBroker = Depends(get_rabbitmq)
):
    """Processing received event data.
    Args:
        event: event data.
        request: request value.
        user_id: Id user
    Returns:
        Execution status.
    """
    user = await user_service.find_one(id=user_id)

    return HTTPStatus.CREATED
