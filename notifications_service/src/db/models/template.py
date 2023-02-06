from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import TEXT

from db.postgres import Base


class Template(Base):
    __tablename__ = "template"

    id = Column(Integer, primary_key=True)
    html = Column(TEXT, nullable=False)
    event_name = Column(String, unique=True, nullable=False)
