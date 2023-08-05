import asyncio
import unittest
from typing import Dict
from datetime import datetime

from TriggerManager import Trigger
from TriggerManager.conditions import BaseCondition


# Auxiliar classes
class TestCondition(BaseCondition):
    value_to_return: bool
    def __init__(self, value_to_return: bool):
        self.value_to_return = value_to_return
    async def check(self, check_time: datetime, context: Dict):
        return self.value_to_return


class TestTrigger(unittest.TestCase):

    loop = None

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self) -> None:
        self.loop.stop()
        self.loop.close()
        return super().tearDown()

    def test_check_true(self):

        async def async_func():
            trigger = Trigger(id="test_id", condition=TestCondition(True), callback=(lambda x: None))
            return await trigger.check(datetime.now())

        res = asyncio.run(async_func())

        self.assertTrue(res)

    def test_check_False(self):

        async def async_func():
            trigger = Trigger(id="test_id", condition=TestCondition(False), callback=(lambda x: None))
            return await trigger.check(datetime.now())

        res = asyncio.run(async_func())

        self.assertFalse(res)


    def test_trigger_callback(self):

        async def async_func():
            event = asyncio.Event()
            callback = lambda time, context: event.set()
            trigger = Trigger(id="test_id", condition=TestCondition(True), callback=callback)
            await trigger.trigger_function(datetime.utcnow())
            return event.is_set()

        res = asyncio.run(async_func())

        self.assertTrue(res)

    def test_check_and_trigger_callback_true(self):

        async def async_func():
            event = asyncio.Event()
            callback = lambda time, context: event.set()
            trigger = Trigger(id="trigger_id", condition=TestCondition(True), callback=callback)
            await trigger.check_and_trigger(datetime.now())
            return event.is_set()

        res = asyncio.run(async_func())

        self.assertTrue(res)

    def test_check_and_trigger_callback_false(self):

        async def async_func():
            event = asyncio.Event()
            callback = lambda: event.set()
            trigger = Trigger(id="test_id", condition=TestCondition(False), callback=callback)
            await trigger.check_and_trigger(datetime.now())
            return event.is_set()

        res = asyncio.run(async_func())

        self.assertFalse(res)