from http import HTTPStatus

from api.v1.events import router
from fastapi.testclient import TestClient
from functional.src.utils.mocks import (
    MockNotificationsService,
    MockRabbitMQBroker,
    MockUserService,
)
from message_broker.rabbitmq.rabbitmq_broker import RabbitMQBroker
from pytest import MonkeyPatch
from services.notifications_service import NotificationsService
from services.user_service import UserService

Client = TestClient(router)


def test_email_notification(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(UserService, "find_one", MockUserService.find_one)
    monkeypatch.setattr(
        NotificationsService, "find_one", MockNotificationsService.find_one
    )
    monkeypatch.setattr(RabbitMQBroker, "produce", MockRabbitMQBroker.produce)

    data = {
        "notification_name": "Notification",
        "priority": 3,
        "data": {
            "movie_name": "The Forest",
            "actor_name": "Pipa Lipa",
            "release_year": 2020,
        },
    }
    response = Client.post("/email/user_id", json=data)

    assert response.json() == HTTPStatus.ACCEPTED
