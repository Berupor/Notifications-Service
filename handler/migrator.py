import logging
from time import sleep

from clickhouse_driver import Client  # type: ignore

logging.basicConfig(level=logging.INFO)

client = Client(host="localhost")
notification_table = "notifications"


def ch_table(client: Client):
    client.execute(
        f"""
        create table if not exists notification(
            id String default generateUUIDv4(),
            status String,
            message String,
            create Datetime default now()
        ) Engine = MergeTree()
        partition by toYYYYMMDD(create)
        order by status
        """)


def init_ch():
    sleep(1)
    ch_table(client)
    logging.info(f"created clickhouse table: {notification_table}")

if __name__ == "__main__":
    init_ch()