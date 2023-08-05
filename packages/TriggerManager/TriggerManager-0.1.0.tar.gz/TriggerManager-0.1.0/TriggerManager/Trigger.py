import asyncio
from datetime import datetime
from dataclasses import dataclass, field
from typing import Union, Callable, Awaitable, Dict

from TriggerManager.conditions import BaseCondition


@dataclass
class Trigger:
    id: str 
    condition: BaseCondition
    callback: Union[Callable, Awaitable]
    is_running_event: asyncio.Event = field(default_factory=(lambda: asyncio.Event()))

    def is_running(self):
        return self.is_running_event.is_set()

    async def check(self, check_time: datetime, context: Dict={}):
        return await self.condition.check(check_time, context)

    async def trigger_function(self, trigger_time: datetime, context: Dict={}):

        if asyncio.iscoroutinefunction(self.callback):
            await self.callback(trigger_time, context)
        else:
            self.callback(trigger_time, context)

    async def check_and_trigger(self, check_time: datetime, context: Dict = {}):
        
        self.is_running_event.set()
        if await self.check(check_time, context):
            await self.trigger_function(check_time)
        self.is_running_event.clear()