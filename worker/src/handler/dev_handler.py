import asyncio
import logging
from time import sleep
import requests

from clickhouse_driver import Client

from worker.src.models.message import NotificationHandler
from worker.src.models.message import MessageHandler

logging.basicConfig(level=logging.INFO)

client = Client(host="localhost")
notification_table = "notifications"
service_url = ""


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
    r = requests.post(f"{service_url}", data=message)
    status_code = r.status_code
    logging.info(status_code)
    return status_code


if __name__ == "__main__":
    print(message_producer())
    logging.info(" [*] Waiting for messages. To exit press CTRL+C")
    sleep(1)