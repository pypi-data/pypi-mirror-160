import unittest

from TriggerManager.conditions import ConditionFactory
from TriggerManager.conditions import TimeCondition


class ConditionFactoryTest(unittest.TestCase):

    def test_create_condition_by_name(self):

        res_condition = ConditionFactory.create_condition_by_name("TimeCondition", {"cron_expression": "* 5 * * *"})

        self.assertTrue(type(res_condition) is TimeCondition)
        self.assertEqual(res_condition.cron_expression, "* 5 * * *")

    def test_create_condition_from_config_dict(self):

        test_config = {
            "type": "TimeCondition",
            "cron_expression": "* 5 * * *"
        }

        res_condition = ConditionFactory.create_condition_from_config_dict(test_config)

        self.assertTrue(type(res_condition) is TimeCondition)
        self.assertEqual(res_condition.cron_expression, "* 5 * * *")



