
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from sizun.errorhandlers.concrete_error import ExternalDependencyError
from .inspection import InspectionABC
from sizun.controllers.aghandler import AGResultHelper


class FEInspector(InspectionABC):

    def __init__(self, aghandler, syntaxhandler, rulehandler):
        self.ag = aghandler
        self.INSPECTION = "FE"
        self.syntax = syntaxhandler
        self.rule = rulehandler
        self.MAX_FOREIGN_REFERENCES = int(self.rule.get_value(self.INSPECTION, "MAX_FOREIGN_REFERENCES"))

    def inspect(self):
        super().inspect()

        _all_methods = self._find_all_methods()
        _all_frefs = self._find_all_foreign_references()

        _fref_counter = dict()

        for _file in _all_methods:

            if _file not in _all_frefs:
                continue

            _fref_counter[_file] = dict()

            _l_frefs = _all_frefs[_file]
            _l_meths = AGResultHelper.get_line_numbers(_all_methods, _file)

            app.logger.debug("file:: {} hat paths starting in:: {}".format(_file, _l_frefs))

            _frefs_in_methods = AGResultHelper.get_lines_witin_sections(_l_frefs, _l_meths)
            _fref_counter[_file] = {k: len(v) for (k, v) in _frefs_in_methods.items()}

            for _method_start_line, _num_frefs in _fref_counter[_file].items():
                if _num_frefs > self.MAX_FOREIGN_REFERENCES:
                    _note = "{} foreign references".format(_num_frefs)
                    _code = AGResultHelper.get_code(_all_methods, _file, _method_start_line)
                    self.note_violation(_file, _method_start_line, _code, _note)
                    self.escalate()

    def _find_all_foreign_references(self):
        _list = self.ag.source_exe(self.syntax.get_foreign_reference_regex())
        return self.ag.to_dict(_list)

    def _find_all_methods(self):
        _list = self.ag.source_exe(self.syntax.get_method_regex())
        return self.ag.to_dict(_list, includecode=True)
