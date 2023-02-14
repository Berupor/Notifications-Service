from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MessageHandler(BaseModel):
    id: str
    status: str
    message: str
    create: datetime


class Notification(BaseModel):
    id_user: Optional[str]
    created_at: Optional[str]
    notification_name: Optional[str]
    priority: Optional[int] = Field(default=0, ge=0, le=3)
    data: Optional[str]
