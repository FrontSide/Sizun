
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from sizun.errorhandlers.concrete_error import ExternalDependencyError
from .inspection import InspectionABC
from sizun.controllers.aghandler import AGResultHelper


class LPLInspector(InspectionABC):

    def __init__(self, aghandler, syntaxhandler, rulehandler):
        self.ag = aghandler
        self.INSPECTION = "LPL"
        self.syntax = syntaxhandler
        self.rule = rulehandler
        self.MAX_PARAMETERS = int(self.rule.get_value(self.INSPECTION, "MAX_PARAMETERS"))

    def inspect(self):
        super().inspect()

        _all_methods = self._find_all_methods()

        for _file, _methods in _all_methods.items():
            for _line, _code in _methods.items():

                try:
                    _parameters = _code[_code.index("("):_code.index(")")].split(",")
                except ValueError:
                    app.logger.error("Could not find patameters in methodstart :: {}".format(_code))

                if len(_parameters) > self.MAX_PARAMETERS:
                    _note = "{} parameters in method in line {}".format(len(_parameters), _line)
                    self.note_violation(_file, _line, _code, _note)
                    self.escalate()

    def _find_all_methods(self):
        _list = self.ag.source_exe(self.syntax.get_method_regex())
        return self.ag.to_dict(_list, includecode=True)
