import asyncio
from datetime import datetime
from tabnanny import check
from typing import Dict, Union, Callable, Awaitable, Dict

class BaseCondition:

    async def check(self, check_time: datetime, context: Dict) -> bool:
        """Check the condition.

        :param checktime: An object with the check time. Some conditions use it because they are time dependent.
        :type checktime: datetime 
        :param context: A dict object with additional data. It can be useful for some conditions that require
        more parameters. 
        :type context: Dict 
        :raises NotImplementedError: When this function is not reimplemented in a subclass.
        :return: True is condition is valid. Otherwise, it returns False. 
        :rtype: bool
        """
        raise NotImplementedError()

    def to_dict(self):

        raise NotImplementedError()