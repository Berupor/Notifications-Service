from datetime import datetime

from pydantic import BaseModel, Field


class Notification(BaseModel):
    id_user: str
    created_at: str
    notification_name: str
    priority: int = Field(default=0, ge=0, le=3)
    data: dict


class NotificationRequest(BaseModel):
    created_at: str
    notification_name: str
    priority: int = Field(default=0, ge=0, le=3)
    data: dict
