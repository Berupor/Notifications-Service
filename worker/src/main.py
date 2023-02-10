import asyncio
import logging
from time import sleep

from models.process import Process

logging.basicConfig(level=logging.INFO)


async def main():
    async with Process() as processing:
        while True:
            processing.broker.message = None

            if await processing.read_queue(queues=["high", "medium", "low"]):
                print(processing.broker.message)

            logging.info("sleep on 10 sec")
            sleep(10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    logging.info(" [*] Waiting for messages. To exit press CTRL+C")
    loop.run_forever()
