import uuid
from typing import Dict

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship

from db.postgres import Base

user_characteristic = Table(
    "user_characteristic",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("characteristic_id", Integer, ForeignKey("characteristic.id")),
)

user_notification = Table(
    "user_notification",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("notification_id", Integer, ForeignKey("notification.id")),
)


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String(255))
    email = Column(String(255), unique=True)
    characteristics = relationship("Characteristic", secondary=user_characteristic)
    notifications = relationship("Notification", secondary=user_notification)

    def to_dict(self) -> Dict:
        return {"name": self.name, "email": self.email}


class Characteristic(Base):
    __tablename__ = "characteristic"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    priority = Column(Integer)
    template_id = Column(Integer, ForeignKey("template.id"))
    data = Column(JSON)
    schedule = relationship("Schedule", back_populates="notifications")
    template = relationship("Template", back_populates="notifications", lazy="joined")


class Template(Base):
    __tablename__ = "template"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    html = Column(String(255), nullable=False)
    notifications = relationship("Notification", back_populates="template")


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True)
    crontab = Column(String(50), nullable=False)
    name = Column(String(255))
    created = Column(DateTime)
    modified = Column(DateTime)
    notifications = relationship("Notification", back_populates="schedule")
