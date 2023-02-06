from typing import Dict

from models.base import BasePydanticModel
from pydantic import Field
from models.user import UserModel

class ResponseEventModel(BasePydanticModel):
    user: UserModel
    template: str

    # Email, push, SMS, etc
    type: str


class RequestEventModel(BasePydanticModel):
    name: str
    urgency: int = Field(default=0, ge=0, le=3)
    data: Dict
