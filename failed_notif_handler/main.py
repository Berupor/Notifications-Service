import logging
import random
from time import sleep
import requests
from datetime import datetime

from clickhouse_driver import Client

from failed_notif_handler.utils.states import JsonFileStorage, State
from core.config import settings

logging.basicConfig(level=logging.INFO)

# client = Client(host=settings.clickhouse.host)
client = Client(host="localhost")
service_email = f"http://{settings.service_url.host}:{settings.service_url.port}/api/v1/notification/email"


def data_from_ch(updated):
    result = client.execute(
        f"""SELECT * FROM default.notification WHERE status LIKE '%error%' AND (create >= toDateTime('{updated}')) 
        ORDER BY create ASC; """,
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


def message_extractor(updated):
    result = data_from_ch(updated=updated)
    messages = data_transform(result)
    return messages


def message_sender(message):
    # user_id = message.user_id
    user_id = random.randint
    result = requests.post(f"{service_email}/{user_id}", data=message)
    status_code = result.status_code
    logging.info(status_code)
    return status_code


if __name__ == "__main__":
    while True:
        state_storage = JsonFileStorage(file_path='json_state')
        state = State(storage=state_storage)
        updated = state.get_state(key='updated')
        messages = message_extractor(updated=updated)
        if messages:
            for message in messages:
                try:
                    message_sender(message)
                    state.set_state(key='updated', value=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                except:
                    logging.warning("the message cannot be proceed by server properly or server offline")
                    break
        logging.info(f"last update {state.get_state(key='updated')}")
        sleep(3)
