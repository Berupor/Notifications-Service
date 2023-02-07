import backoff


class Extract:
    def __init__(self, connect):
        self.pg_conn = connect

    def execute_query(self, query: str):
        """Функция выполнения запросов к postgresql"""
        """
        :param query: запрос на получения данных
        :return: результат выполнения
        """
        curs = self.pg_conn.cursor()
        curs.execute(query)
        return curs

    def read_db(self, query: str, batch_size: int = 100) -> list:
        """Функция выполнения запросов к хранилищу"""
        """
        :param query: запрос к БД
        :param batch_size: объем считываемой пачки данных
        :return: список полученных данных
        """
        curs = self.execute_query(query)
        while raws := curs.fetchmany(batch_size):
            yield raws
