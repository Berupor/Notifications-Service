import asyncio
import logging
from time import sleep

import aioschedule as schedule
from etl.base_etl import Etl
from models.notifications import NotificationRequest

logging.basicConfig(level=logging.INFO)


async def main():
    logging.info("start process")
    async with Etl() as etl:
        async for raws in etl.extract.read_db(
            query="select id, crontab, created from notification_database.public.schedule",
            batch_size=10,
        ):
            data_schedulers = await etl.transform.validate_shcedule(raws)
            id_schedule = await etl.transform.compare_shcedule(data_schedulers)
            if id_schedule:
                async for data in etl.extract.read_db(
                    query=f"""select user_id, to_char(created, 'YYYY-MM-DD HH24:MI:SS') as created_at,
                                name as notification_name, priority, data from notification
                                INNER JOIN user_notification un on notification.id = un.notification_id
                                where schedule_id in ('{"','".join(id_schedule)}')""",
                    batch_size=10,
                ):
                    valid_notifications = await etl.transform.validate_notifications(
                        data
                    )
                    for notification in valid_notifications:
                        await etl.load.send_request(
                            url_path=f"/api/v1/notification/email/{notification.id_user}",
                            data=NotificationRequest(**notification.dict()).dict(),
                        )


if __name__ == "__main__":
    schedule.every(1).minutes.do(main)
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(schedule.run_pending())
        logging.info("wait sheduler")
        sleep(1)
