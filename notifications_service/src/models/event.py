from pydantic import Field

from models.base import BasePydanticModel
from models.user import UserModel


class ResponseEventModel(BasePydanticModel):
    user: UserModel
    template: str

    # Email, push, SMS, etc
    type: str
    data: dict


class RequestEventModel(BasePydanticModel):
    notification_name: str
    priority: int = Field(default=0, ge=0, le=3)
    data: dict
