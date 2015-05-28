
"""
Sizun
MIT License
(C) 2015 David Rieger
"""
from .inspection import InspectionABC


class MCInspector(InspectionABC):

    def __init__(self, aghandler, syntaxhandler, rulehandler):
        self.ag = aghandler
        self.INSPECTION = "MC"
        self.syntax = syntaxhandler
        self.rule = rulehandler
        self.MAX_OBJECTS_IN_MESSAGE_CHAIN = int(self.rule.get_value(self.INSPECTION, "MAX_OBJECTS_IN_MESSAGE_CHAIN"))

    def inspect(self):
        super().inspect()

        _all_chains = self._find_all_message_chains()

        for _file, _chain in _all_chains.items():
            for _line, _code in _chain.items():

                _num_objects = len(_code.split("."))

                if _num_objects > self.MAX_OBJECTS_IN_MESSAGE_CHAIN:
                    _note = "{} objects".format(_num_objects)
                    self.note_violation(_file, _line, _code, _note)
                    self.escalate()

    def _find_all_message_chains(self):
        _list = self.ag.source_exe(self.syntax.get_message_chain_regex())
        return self.ag.to_dict(_list, includecode=True)
