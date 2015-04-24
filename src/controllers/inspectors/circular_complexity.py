
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from errorhandlers.concrete_error import ExternalDependencyError
from .inspection import InspectionABC

class CCInspector(InspectionABC):

    def __init__(self, aghandler, syntaxhandler, rulehandler):
        self.ag = aghandler
        self.INSPECTION = "CC"
        self.syntax = syntaxhandler
        self.rule = rulehandler
        self.MAX_COMPLEXITY = int(self.rule.get_value(self.INSPECTION, "MAX_COMPLEXITY"))

    def inspect(self):
        super().inspect()

        _all_methods = self._find_all_methods()
        _all_ifs = self._find_all_ifs()

        _ifs_counter = dict()

        for _file in _all_methods:

            if _file not in _all_ifs:
                continue

            _ifs_counter[_file] = dict()

            _l_ifs = _all_ifs[_file]
            _l_meths = [element["line"] for element in _all_methods[_file]]

            for _l_meth in _l_meths:

                # List comprehension to check whether line (here if statement) is within a method
                # TODO: outsource this listcomprehension since it might be needed in other inspectors as well
                try:
                    _l_next_meth = _l_meths[_l_meths.index(_l_meth)+1]
                    _ifs_in_meth = [_l_if for _l_if in _l_ifs if _l_if > _l_meth and _l_if < _l_next_meth]
                except IndexError:
                    # If last method
                    _ifs_in_meth = [_l_if for _l_if in _l_ifs if _l_if > _l_meth]

                _ifs_counter[_file][_l_meth] = len(_ifs_in_meth)

                if _ifs_counter[_file][_l_meth] > self.MAX_COMPLEXITY:

                    # Get code of method start where rule violation happens
                    # TODO: outsource to ag handler!!
                    for e in _all_methods[_file]:
                        if e["line"] is _l_meth:
                            _code = e["code"]

                    self.note_violation(_file, _l_meth, _code, "complexity is {}".format(_ifs_counter[_file][_l_meth]))
                    self.escalate()

    def _find_all_ifs(self):
        _list = self.ag.source_exe(self.syntax.get_if_regex())
        return self.ag.to_simple_dic(_list)

    def _find_all_methods(self):
        _list = self.ag.source_exe(self.syntax.get_method_regex())
        return self.ag.to_full_dic(_list)
