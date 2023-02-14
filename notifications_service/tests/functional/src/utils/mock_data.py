import uuid
from typing import Dict
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID = uuid.uuid4()
    name: str
    email: str

    def to_dict(self):
        return {"name": self.name, "email": self.email}


class Template(BaseModel):
    html: str


class Notification(BaseModel):
    template: Template
    data: Dict


mock_user = User(name="MockUser", email="mock@example.com")
mock_template = Template(html="Mock Html")
mock_notification = Notification(template=mock_template, data={"movie": "mock_movie"})
