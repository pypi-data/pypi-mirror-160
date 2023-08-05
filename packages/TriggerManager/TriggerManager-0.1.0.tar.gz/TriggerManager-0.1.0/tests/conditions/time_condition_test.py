import asyncio
import unittest
from datetime import datetime

from TriggerManager.conditions import TimeCondition
from TriggerManager.conditions.TimeCondition import InvalidCronExpressionError
from TriggerManager.conditions.TimeCondition import CronFunction


class TimeTriggerTest(unittest.TestCase):

    def test_valid_cron_expressions(self):

        test_expressions = [
            "* * * * *",
            "5 * * * *",
            "5 0 * 8 *",
            "15 14 1 * *",
            "0 22 * * 5",
            "23 20 * * *"
        ]

        try:
            for expression in test_expressions:
                TimeCondition(expression)
        except Exception as e:
            self.fail(f"Raised exception: {e}")

    def test_invalid_cron_expressions(self):

        test_expressions = [
            "* *",
            "70 * * * *",
            "* 30 * * *",
            "* * 32 * *",
            "* * * 13 *",
            "* * * * 8"
        ]

        for test_expression in test_expressions:

            with self.assertRaises(InvalidCronExpressionError) as ctx:
                TimeCondition(test_expression)

    def test_cron_functions_true(self):

        test_date = datetime(year=2022, month=6, day=7, hour=10, minute=20)

        cron_exprs = [
            "* * * * *",
            "20 * * * *",
            "* 10 * * *",
            "* * 7 * *",
            "* * * 6 *",
            "* * * * 2",
            "20 10 7 6 2",
            "* 10 7 6 2",
            "20 * 7 6 2",
            "20 * 7 6 *",
            "20 * 7 * 2",
        ]

        for cron_expr in cron_exprs:
            cron_function = CronFunction(cron_expr)
            self.assertTrue(cron_function(test_date))

    def test_cron_functions_false(self):

        test_date = datetime(year=2022, month=6, day=7, hour=10, minute=20)

        cron_exprs = [
            "30 * * * *",
            "* 12 * * *",
            "* * 8 * *",
            "* * * 7 *",
            "* * * * 1"
        ]

        for cron_expr in cron_exprs:
            cron_function = CronFunction(cron_expr)
            self.assertFalse(cron_function(test_date))

    def test_check_true(self):

        test_date = datetime(2022, 12, 5)

        async def async_func():
            res_event = asyncio.Event()
            time_condition = TimeCondition("* * 5 * *")
            return await time_condition.check(test_date)

        res = asyncio.run(async_func())

        self.assertTrue(res)

    def test_check_false(self):

        test_date = datetime(2022, 12, 5)

        async def async_func():
            time_trigger = TimeCondition("* * 6 * *")
            await time_trigger.check(test_date)

        res = asyncio.run(async_func())

        self.assertFalse(res)
