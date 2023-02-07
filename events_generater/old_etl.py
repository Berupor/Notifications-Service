# import requests
# import psycopg2
# import croniter
# from datetime import datetime
# import json
# import logging
# from datetime import datetime
# from http import HTTPStatus
#
# from core.config import settings
#
#
# class Etl:
#     def __enter__(self, pg_host, pg_port, pg_database, pg_user, pg_password):
#         self.pg_conn = psycopg2.connect(
#             host=pg_host,
#             port=pg_port,
#             database=pg_database,
#             user=pg_user,
#             password=pg_password,
#         )
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.pg_conn.close()
#
#     def get_crontab(self):
#
#
#     @backoff()
#     def query_extract(self, query: str):
#         """Функция выполнения запросов к postgresql"""
#         """
#         :param query: запрос на получения данных
#         :return: результат выполнения
#         """
#         curs = self.pg_conn.cursor()
#         curs.execute(query)
#         return curs
#
#     def extract(self, queries: dict, batch_size: int = 100) -> list:
#         """Функция выполнения запросов к postgresql"""
#         """
#         :param queries: словарь, содержащий запросы ко всем таблицам
#         :param batch_size: объем считываемой пачки данных
#         :return: список полученных данных
#         """
#         for table_name in queries:
#             # определение места, откуда в текущей момент будут обрабатываться данные
#             self.state.set_state("current_table", table_name)
#             # определение даты последнего изменения
#             last_modified_state = self.state.get_state(table_name + "_last_modified")
#             last_modified = last_modified_state if last_modified_state else str(datetime.min)
#             # добавление данными запроса
#             valid_query = (
#                     queries[table_name]
#                     + f" '{last_modified}' "
#                     + "GROUP BY fw.id ORDER BY fw.modified;"
#             )
#             curs = self.query_extract(valid_query)
#             logging.info(
#                 f"Получил данные из таблицы {table_name} where modified > {last_modified}"
#             )
#             # Создание списка для записи результатов запросов
#             while raws := curs.fetchmany(batch_size):
#                 yield raws
#             if self.state.get_state(self.state.get_state("current_table") + "_status") == "True":
#                 self.state.set_state(table_name + "_last_modified", str(datetime.now()))
#
#     @backoff()
#     def transform(self, values: list) -> str:
#         """Функция преобразования данных"""
#         """
#         :param values: список данных
#         :return: данные преобразованные в формат для занесения
#         """
#         result = ""
#         # валидация данных и преобразование к формату для занесения в elasticsearch
#         for raws in values:
#             raw_data = RawData(
#                 **{key: raws[i] for i, key in enumerate(RawData.__fields__.keys())}
#             )
#             header_data = json.dumps(
#                 {"index": {"_index": "movies", "_id": f"{raw_data.id}"}}
#             )
#             processed_data = ProcessedData(
#                 id=raw_data.id,
#                 title=raw_data.title,
#                 description=raw_data.description,
#                 imdb_rating=raw_data.rating,
#                 genre=raw_data.genres,
#                 actors_names=[
#                     person["person_name"]
#                     for person in raw_data.persons
#                     if person["person_role"] == "actor"
#                 ],
#                 writers_names=[
#                     person["person_name"]
#                     for person in raw_data.persons
#                     if person["person_role"] == "writer"
#                 ],
#                 actors=[
#                     {"id": person["person_id"], "name": person["person_name"]}
#                     for person in raw_data.persons
#                     if person["person_role"] == "actor"
#                 ],
#                 writers=[
#                     {"id": person["person_id"], "name": person["person_name"]}
#                     for person in raw_data.persons
#                     if person["person_role"] == "writer"
#                 ],
#             )
#             result += header_data + "\n" + processed_data.json() + "\n"
#         logging.info("Данные успешно обработаны!")
#         return result
#
#     @backoff()
#     def load(self, processed_data: str):
#         """Функция занесения данных в elasticsearch"""
#         """
#         :param processed_data: данные для занесения в базу
#         """
#         result = self.pull_elastic(processed_data)
#         status_name = self.state.get_state("current_table") + "_status"
#         if result.status_code == HTTPStatus.OK and (
#                 self.state.get_state(status_name) == "True" or self.state.get_state(status_name) is None
#         ):
#             logging.info("Данные занесены в elasticsearch")
#             self.state.set_state(status_name, "True")
#         else:
#             logging.info("Ошибка занесения в elasticsearch")
#             self.state.set_state(status_name, "False")
