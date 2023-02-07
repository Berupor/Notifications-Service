from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import croniter
from models.schedule import Schedule

# now = datetime.datetime.now()
# sched = '1 15 1,15 * *'    # at 3:01pm on the 1st and 15th of every month
# cron = croniter.croniter(sched, now)
#
# for i in range(4):
#     nextdate = cron.get_next(datetime.datetime)
#     print nextdate


class Transform:
    def convert_shcedule(self, data: List[Tuple]) -> List[Schedule]:
        return [
            Schedule(
                **{key: row[i] for i, key in enumerate(Schedule.__fields__.keys())}
            )
            for row in data
        ]

    def compare_shcedule(self, data: List[Schedule]) -> Optional[List[str]]:
        use_schedule = []
        now = datetime.now()
        for raw in data:
            cron = croniter.croniter(raw.crontab, now)
            next_execute = cron.get_next(datetime)
            if now <= next_execute and next_execute <= (now + timedelta(minutes=1)):
                use_schedule.append(raw.id)
        if use_schedule:
            return use_schedule
        return None
