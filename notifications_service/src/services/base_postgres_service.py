from sqlalchemy.future import select

from db.postgres import async_session


class BaseService:
    _model = None

    def __init__(self):
        self._session = async_session

    async def find_one(self, **kwargs):
        async with self._session() as session:
            query = select(self._model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar()

    async def find(self, **kwargs):
        async with self._session() as session:
            return session.query(self._model).filter_by(**kwargs).all()
