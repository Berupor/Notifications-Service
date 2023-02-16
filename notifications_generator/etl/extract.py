from typing import AsyncGenerator


class Extract:
    def __init__(self, connect):
        self.pg_conn = connect

    async def execute_query(self, query: str):
        """Функция выполнения запросов к postgresql"""
        """
        :param query: запрос на получения данных
        :return: результат выполнения
        """
        return await self.pg_conn.execute(query)

    async def read_db(self, query: str, batch_size: int = 100) -> AsyncGenerator:
        """Функция выполнения запросов к хранилищу"""
        """
        :param query: запрос к БД
        :param batch_size: объем считываемой пачки данных
        :return: список полученных данных
        """
        curs = await self.execute_query(query)
        while raws := curs.fetchmany(batch_size):
            yield raws
