import logging
from http import HTTPStatus
from json import dumps
from urllib.parse import urljoin

import aiohttp
import backoff


class Load:
    def __init__(self, base_url: str):
        self.base_url = base_url

    @backoff.on_exception(
        backoff.expo,
        (
            aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.ServerDisconnectedError,
        ),
        max_time=1000,
        max_tries=10,
    )
    async def send_request(self, url_path: str, data: dict):
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=urljoin(self.base_url, url_path),
                data=dumps(data),
                headers={"Content-Type": "application/json"},
            )
        if response.status == HTTPStatus.OK:
            logging.info("Notification was sent successfully.")
        else:
            logging.error("Notification send error")
