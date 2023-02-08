import asyncio
# import schedule
import aioschedule as schedule
from datetime import datetime

from etl.base_etl import Etl
from models.event import EventRequest
from time import sleep


async def main():
    async with Etl() as etl:
        async for raws in etl.extract.read_db(
            query="select * from notification_database.public.schedule", batch_size=10
        ):
            data_schedulers = await etl.transform.validate_shcedule(raws)
            id_schedule = await etl.transform.compare_shcedule(data_schedulers)
            if id_schedule:
                async for data in etl.extract.read_db(
                    query=f"""select id_user, name, priority, data, to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') as created_at from events where id_schedule in ('{"','".join(id_schedule)}')""",
                    batch_size=10,
                ):
                    valid_events = await etl.transform.validate_events(data)
                    for event in valid_events:
                        await etl.load.send_request(
                            url_path=f"/api/v1/notification/email/{event.id_user}",
                            data=EventRequest(**event.dict()).dict(),
                        )


if __name__ == "__main__":
    schedule.every(1).minutes.do(main)
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(schedule.run_pending())
        sleep(1)

