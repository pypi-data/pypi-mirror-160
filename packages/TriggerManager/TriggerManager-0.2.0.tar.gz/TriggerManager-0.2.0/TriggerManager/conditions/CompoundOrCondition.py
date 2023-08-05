from lib2to3.pytree import Base
from typing import Dict, List
from datetime import datetime

from TriggerManager.conditions import BaseCondition



class CompoundOrCondition(BaseCondition):

    conditions: List[BaseCondition] = []

    def __init__(self, conditions: List[BaseCondition]):

        self.conditions = conditions

    async def check(self, check_time: datetime, context: Dict) -> bool:

        # Return true with first valid check
        for condition in self.conditions:
            if await condition.check(check_time, context):
                return True
        
        # All conditions fail
        return False

    def to_dict(self):

        return {
            "type": "CompoundOrCondition",
            "conditions": [condition.to_dict() for condition in self.conditions]
        }
