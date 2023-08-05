import asyncio
import unittest
from typing import Dict
from datetime import datetime

from TriggerManager.conditions import BaseCondition
from TriggerManager.conditions import CompoundOrCondition


class TestCondition(BaseCondition):
    event: asyncio.Event
    value_to_return: bool
    def __init__(self, value_to_return: bool):
        self.event = asyncio.Event()
        self.value_to_return = value_to_return
    async def check(self, check_time: datetime, context: Dict):
        self.event.set()
        return self.value_to_return


class CompoundOrConditionTest(unittest.TestCase):

    def test_valid_with_first_condition_and_second_one_not_checked(self):

        first_condition = TestCondition(True)
        second_condition = TestCondition(True)

        compound_or_condition = CompoundOrCondition([first_condition, second_condition])

        async def async_func():
            return await compound_or_condition.check(datetime.now(), {})

        res = asyncio.run(async_func())

        self.assertTrue(res)
        self.assertTrue(first_condition.event.is_set())
        self.assertFalse(second_condition.event.is_set())

    def test_valid_with_second_condition_and_both_checked(self):

        first_condition = TestCondition(False)
        second_condition = TestCondition(True)

        compound_or_condition = CompoundOrCondition([first_condition, second_condition])

        async def async_func():
            return await compound_or_condition.check(datetime.now(), {})

        res = asyncio.run(async_func())

        self.assertTrue(res)
        self.assertTrue(first_condition.event.is_set())
        self.assertTrue(second_condition.event.is_set())

