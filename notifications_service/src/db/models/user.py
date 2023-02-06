import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from typing import Dict
from db.postgres import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String)
    email = Column(String, unique=True)

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'email': self.email
        }
