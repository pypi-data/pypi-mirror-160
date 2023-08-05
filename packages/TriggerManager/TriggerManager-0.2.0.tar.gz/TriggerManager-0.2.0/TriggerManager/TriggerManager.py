import asyncio
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import Union, Callable, Awaitable, List, Dict

from TriggerManager.conditions import BaseCondition
from TriggerManager import Trigger


class TriggerManager:

    trigger_list: List[Trigger]
    stop_event: asyncio.Event()
    last_time_checked: datetime
    check_interval: int = 10

    def __init__(self):
        self.trigger_list = []
        self.stop_event = asyncio.Event()
        self.last_time_checked = None

    def add_trigger(self, trigger: Trigger):
        self.trigger_list.append(trigger)

    def stop_trigger_loop(self):
        self.stop_event.set()

    async def start_trigger_loop(self):

        async def task_func():
            while not self.stop_event.is_set():
                current_datetime = datetime.now().replace(second=0, microsecond=0)
                # Only check the trigger when the minutes change.
                if self.last_time_checked is None or current_datetime > self.last_time_checked: 
                    self.last_time_checked = current_datetime
                    await self.check_triggers()
                
                await asyncio.sleep(self.check_interval)

        asyncio.create_task(task_func())

    async def check_triggers(self):
        logging.info(f"Checking triggers at {self.last_time_checked}")

        task_list = [
            trigger.check_and_trigger(self.last_time_checked)
            for trigger in self.trigger_list if not trigger.is_running()
        ]

        asyncio.gather(*task_list)