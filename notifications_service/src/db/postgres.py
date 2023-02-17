from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from core.config import settings

db_uri = (
    "postgresql+asyncpg://"
    f"{settings.postgres.user}:{settings.postgres.password}@"
    f"{settings.postgres.host}:{settings.postgres.port}/"
    f"{settings.postgres.dbname}"
)
db = create_async_engine(db_uri)
async_session = sessionmaker(db, expire_on_commit=False, class_=AsyncSession)

db_session = scoped_session(async_session)

Base = declarative_base()
Base.query = db_session.query_property()
