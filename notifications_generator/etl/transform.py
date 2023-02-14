from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import croniter  # type: ignore
from models.notifications import Notification
from models.schedule import Schedule


class Transform:
    async def validate_shcedule(self, data: List[Tuple]) -> List[Schedule]:
        return [
            Schedule(
                **{key: row[i] for i, key in enumerate(Schedule.__fields__.keys())}
            )
            for row in data
        ]

    async def validate_notifications(self, data: List[Tuple]) -> List[Notification]:
        return [
            Notification(
                **{key: row[i] for i, key in enumerate(Notification.__fields__.keys())}
            )
            for row in data
        ]

    async def compare_shcedule(self, data: List[Schedule]) -> Optional[List[str]]:
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
