import xml.etree.ElementTree as ET

from urh.simulator.SimulatorCounterAction import SimulatorCounterAction
from urh.simulator.SimulatorItem import SimulatorItem
from urh.simulator.SimulatorProtocolLabel import SimulatorProtocolLabel
from urh.simulator.SimulatorRule import SimulatorRule, SimulatorRuleCondition, ConditionType
from urh.simulator.SimulatorTriggerCommandAction import SimulatorTriggerCommandAction


class SimulatorGotoAction(SimulatorItem):
    def __init__(self):
        super().__init__()
        self.goto_target = None  # type: str

    def set_parent(self, value):
        if value is not None:
            assert value.parent() is None or isinstance(value, SimulatorRuleCondition)

        super().set_parent(value)

    @property
    def target(self):
        return self.simulator_config.item_dict[self.goto_target] if self.validate() else None

    def validate(self):
        target = self.simulator_config.item_dict.get(self.goto_target, None)
        return self.is_valid_goto_target(self.goto_target, target)

    def get_valid_goto_targets(self):
        return [
            key
            for key, value in self.simulator_config.item_dict.items()
            if value != self
            and SimulatorGotoAction.is_valid_goto_target(key, value)
        ]

    def to_xml(self) -> ET.Element:
        attributes = {}
        if self.goto_target is not None:
            attributes["goto_target"] = self.goto_target

        return ET.Element("simulator_goto_action", attrib=attributes)

    @classmethod
    def from_xml(cls, tag: ET.Element):
        result = SimulatorGotoAction()
        result.goto_target = tag.get("goto_target", None)
        return result

    @staticmethod
    def is_valid_goto_target(caption: str, item: SimulatorItem):
        if item is None:
            return False
        if isinstance(item, (SimulatorProtocolLabel, SimulatorRule)):
            return False
        if isinstance(item, SimulatorRuleCondition) and item.type != ConditionType.IF:
            return False
        if isinstance(item, SimulatorCounterAction):
            return False
        return not isinstance(
            item, SimulatorTriggerCommandAction
        ) or not caption.endswith("rc")
