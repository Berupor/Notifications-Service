import logging
import random
from time import sleep
from datetime import datetime

import requests
from clickhouse_driver import Client

from utils.states import JsonFileStorage, State
from core.config import settings
from models.notification import Notification

logging.basicConfig(level=logging.INFO)

client = Client(host=settings.clickhouse.host)
service_email = (
    f"http://{settings.fastapi.host}:{settings.fastapi.port}/api/v1/notification/email"
)


def data_from_ch(updated):
    result = client.execute(
        f"""SELECT * FROM default.notification WHERE status LIKE '%error%' AND (create >= toDateTime('{updated}')) 
        ORDER BY create ASC; """,
        with_column_types=True,
    )
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


def messages_extractor(updated: str):
    result = data_from_ch(updated=updated)
    messages = data_transform(result)
    return messages


def message_to_notification(message: dict):
    notification = Notification()
    notification.user_id = message["user"]["user_id"]
    notification.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notification.notification_name = message["notification_name"]
    notification.priority = 3  # the higthest priority
    notification.data = message["data"]
    return notification


def notification_sender(notification: Notification):
    user_id = random.randint
    result = requests.post(f"{service_email}/{user_id}", data=notification)
    status_code = result.status_code
    logging.info(status_code)
    return status_code


if __name__ == "__main__":
    while True:
        sleep(10)
        state_storage = JsonFileStorage(file_path="json_state")
        state = State(storage=state_storage)
        updated = state.get_state(key="updated")
        if not updated:
            state.set_state(
                key="updated",
                value=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            )
            updated = state.get_state(key="updated")
        messages = messages_extractor(updated=updated)
        if messages:
            for message in messages:
                try:
                    notification = message_to_notification(message)
                    status_code = notification_sender(notification)
                    state.set_state(
                        key="updated",
                        value=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    )
                    logging.info(status_code)
                except:
                    logging.warning(
                        "the message cannot be proceed by server properly or server is offline"
                    )
                    break
        logging.info(f"last update {state.get_state(key='updated')}")
