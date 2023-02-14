from json import dumps
from typing import Dict
import backoff

import asynch


class Clickhouse:
    def __init__(self, host: str, port: int, user: str = "default", password: str = ""):
        self.host = host
        self.port = port
        # database = "default"
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.table = "notification"

    @backoff.on_exception(
        backoff.expo,
        (
                ConnectionError
         ),
        max_time=1000,
        max_tries=10,
    )
    async def connect(self):
        self.connection = await asynch.connect(
            host=self.host, port=self.port, user=self.user, password=self.password
        )
        self.cursor = self.connection.cursor()

    async def create_table(self):
        await self.cursor.execute(
            f"""
        create table if not exists {self.table}(
            id String default generateUUIDv4(),
            status String,
            message String,
            create Datetime default now()
        ) Engine = MergeTree()
        partition by toYYYYMMDD(create)
        order by status
        """
        )

    async def insert(self, table: str, data: list):
        return await self.cursor.execute(
            f"INSERT INTO {table}(status, message) VALUES", data
        )



    async def validate_format(self, status: str, message: dict) -> Dict:
        return {"status": status, "message": dumps(message)}
