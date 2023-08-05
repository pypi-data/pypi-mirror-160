from datetime import datetime
import re
from typing import Callable, Dict
from TriggerManager.conditions import BaseCondition

class InvalidCronExpressionError(Exception):
    pass

class CronFunction:
    regular_expression: str = "^(\S+) (\S+) (\S+) (\S+) (\S+)$"
    match_function: Callable = None

    def __init__(self, expression: str):

        if(match := re.match(self.regular_expression, expression)) is not None:
            exprs = match.groups()
            self.match_function = self.create_match_function(
                self.parse_minute_expression(exprs[0]),
                self.parse_hour_expression(exprs[1]),
                self.parse_day_expression(exprs[2]),
                self.parse_month_expression(exprs[3]),
                self.parse_weekday_expression(exprs[4]),
            )
        else:
            raise InvalidCronExpressionError(f"Not valid cron expression: {expression}")

    def __call__(self, date_to_check: datetime) -> bool:
        return self.match_function(date_to_check)

    @staticmethod
    def create_match_function(
        minute_func: Callable,
        hour_func: Callable,
        day_func: Callable,
        month_func: Callable,
        weekday_func: Callable
    ) -> Callable[[datetime], bool]:
        return (
            lambda date: minute_func(date.minute) \
            and hour_func(date.hour) \
            and day_func(date.day) \
            and month_func(date.month) \
            and weekday_func(date.isoweekday())
        )

    @staticmethod
    def parse_common_expression(name: str, expr: str, min: int, max: int) -> Callable:
        if expr == "*":
            return (lambda value: True)
        elif re.match("^\d+$", expr) is not None:
            expected_value = int(expr)
            if expected_value >=min and expected_value <= max:
                return (lambda input_minute: input_minute == expected_value)
            else:
                raise InvalidCronExpressionError(f"Not valid {name} value: {expr}")
        else:
            raise InvalidCronExpressionError(f"Not valid {name} value: {expr}")

    @staticmethod
    def parse_minute_expression(expr: str) -> Callable:
        return CronFunction.parse_common_expression("minute", expr, 0, 59)

    @staticmethod
    def parse_hour_expression(expr: str) -> Callable:
        return CronFunction.parse_common_expression("hour", expr, 0, 23)

    @staticmethod
    def parse_day_expression(expr: str) -> Callable:
        return CronFunction.parse_common_expression("day", expr, 1, 31)

    @staticmethod
    def parse_month_expression(expr: str) -> Callable:
        return CronFunction.parse_common_expression("month", expr, 1, 12)

    @staticmethod
    def parse_weekday_expression(expr: str) -> Callable:
        return CronFunction.parse_common_expression("weekday", expr, 1, 7)


class TimeCondition(BaseCondition):

    cron_expression: str
    cron_function: Callable

    def __init__(self, cron_expression: str):

        self.cron_expression = cron_expression
        self.cron_function = CronFunction(cron_expression)

    async def check(self, check_time: datetime, context: Dict={}) -> bool:

        return self.cron_function(check_time)

    async def to_dict(self):

        return {
            "type": "TimeCondition",
            "cron_expression": self.cron_expression
        }



