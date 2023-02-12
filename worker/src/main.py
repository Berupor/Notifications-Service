import asyncio
import logging
from time import sleep

from models.process import Process
from models.recipier import Recipier

logging.basicConfig(level=logging.INFO)


async def main():
    async with Process() as processing:
        while True:
            processing.broker.message = None

            if await processing.read_queue(queues=["high", "medium", "low"]):
                async with Recipier(type=processing.broker.message["type"]) as recipier:
                    async for message in recipier.service.create_message(
                        users_to=[processing.broker.message["user"]["email"]],
                        data=processing.broker.message["data"],
                        template=processing.broker.message["template"],
                    ):
                        response = await recipier.service.send_message(message)
                        await processing.check_status(response=response)

                        result_insert = await processing.storage.insert(
                            table=processing.storage.table,
                            data=[
                                await processing.storage.validate_format(
                                    status=processing.status,
                                    message=processing.broker.message,
                                )
                            ],
                        )

                        if result_insert:
                            logging.info("data insert successfully")
                        else:
                            logging.info("data insert with ERROR")

            logging.info("sleep on 10 sec")
            sleep(10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    logging.info(" [*] Waiting for messages. To exit press CTRL+C")
    loop.run_forever()
