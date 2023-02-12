import asyncio
import logging
import random
from time import sleep
import requests

from clickhouse_driver import Client

from worker.src.models.message import NotificationHandler
from worker.src.models.message import MessageHandler

logging.basicConfig(level=logging.INFO)

client = Client(host="localhost")
service_url = "http://0.0.0.0:8001/api/v1/notification/email"


def data_from_ch():
    result = client.execute(f"""SELECT * FROM default.notification WHERE status LIKE '%error%'""",
                                  with_column_types=True)
    return result

def data_transform(result):
    raw_data = result[0]
    raw_columns = result[1]
    columns = [column[0] for column in raw_columns]
    messages = list()
    for i in raw_data:
        message = dict(zip(columns, [value for value in i]))
        messages.append(message)
    return messages


def message_producer():
    result = data_from_ch()
    messages = data_transform(result)
    return messages


def message_sender(message):
    #user_id = message.user_id
    user_id = random.randint
    result = requests.post(f"{service_url}/{user_id}", data=message)
    status_code = result.status_code
    logging.info(status_code)
    return status_code


if __name__ == "__main__":
    while True:
        state_storage = JsonFileStorage(file_path='json_state')
        state = State(storage=state_storage)
    messages = message_producer()
    for message in messages:
        message_sender(message)
    logging.info(" [*] Waiting for messages. To exit press CTRL+C")
    sleep(1)