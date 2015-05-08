
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
        self.INSPECTION = "CC"
        self.syntax = syntaxhandler
        self.rule = rulehandler
        self.MAX_COMPLEXITY = int(self.rule.get_value(self.INSPECTION, "MAX_COMPLEXITY"))

    def inspect(self):
        super().inspect()

        _all_methods = self._find_all_methods()
        _all_paths = self._find_all_paths()

        _path_counter = dict()

        for _file in _all_methods:

            if _file not in _all_paths:
                continue

            _path_counter[_file] = dict()

            _l_paths = _all_paths[_file]
            _l_meths = AGResultHelper.get_line_numbers(_all_methods, _file)

            app.logger.debug("file:: {} hat paths starting in:: {}".format(_file, _l_paths))

            _paths_in_methods = AGResultHelper.get_lines_witin_sections(_l_paths, _l_meths)
            _path_counter[_file] = {k: len(v) for (k, v) in _paths_in_methods.items()}

            for _method_start_line, _num_paths in _path_counter[_file].items():
                if _num_paths > self.MAX_COMPLEXITY:
                    _note = "complexity is {}".format(_num_paths)
                    _code = AGResultHelper.get_code(_all_methods, _file, _method_start_line)
                    self.note_violation(_file, _method_start_line, _code, _note)
                    self.escalate()

    def _find_all_paths(self):
        _list = self.ag.source_exe(self.syntax.get_flowpath_regex())
        return self.ag.to_dict(_list)

    def _find_all_methods(self):
        _list = self.ag.source_exe(self.syntax.get_method_regex())
        return self.ag.to_dict(_list, includecode=True)
