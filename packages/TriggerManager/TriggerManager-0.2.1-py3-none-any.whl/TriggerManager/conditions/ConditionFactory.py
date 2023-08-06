from typing import Dict
import importlib

from TriggerManager.conditions import BaseCondition

class ConditionFactory:

    @staticmethod
    def create_condition_by_name(condition_name: str, params: Dict) -> BaseCondition:

        module = importlib.import_module("TriggerManager.conditions")
        condition_class = getattr(module, condition_name)

        return condition_class(**params)

    @staticmethod
    def create_condition_from_config_dict(config: Dict) -> BaseCondition:

        condition_name = config["type"]
        params = {k:v for k,v in config.items() if k != "type"}

        return ConditionFactory.create_condition_by_name(condition_name, params)