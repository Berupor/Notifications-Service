from datetime import datetime

from pydantic import BaseModel, Field


class Event(BaseModel):
    id_user: str
    name: str
    priority: int = Field(default=0, ge=0, le=3)
    data: dict
    created_at: str


class EventRequest(BaseModel):
    created_at: str
    name: str
    priority: int = Field(default=0, ge=0, le=3)
    data: dict
