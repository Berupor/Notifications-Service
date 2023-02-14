from datetime import datetime

from pydantic import BaseModel


class Schedule(BaseModel):
    id: str
    crontab: str
    created: datetime
