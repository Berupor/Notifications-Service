from sqlalchemy.future import select

from db.postgres import Base, async_session


class BaseService:
    _model: Base = None

    def __init__(self):
        self._session = async_session

    async def find_one(self, **kwargs):
        async with self._session() as session:
            query = select(self._model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar()
