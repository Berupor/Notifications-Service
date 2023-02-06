from base import BasePydanticModel
from user import UserModel
from pydantic import Field
from typing import Dict


class ResponseEventModel(BasePydanticModel):
    user: UserModel
    template: str

    # Email, push, SMS, etc
    type: str


class RequestEventModel(BasePydanticModel):
    name: str
    urgency: int = Field(default=0, ge=0, le=3)
    data: Dict
