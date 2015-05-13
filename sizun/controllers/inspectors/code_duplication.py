
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from sizun.errorhandlers.concrete_error import ExternalDependencyError
from .inspection import InspectionABC
from sizun.controllers.aghandler import AGResultHelper
from sizun.controllers.linegrabber import LineGrabber


class CDInspector(InspectionABC):

    def __init__(self, pmdhandler, rulehandler, linegrabber):
        self.pmd = pmdhandler
        self.INSPECTION = "CD"
        self.rule = rulehandler
        self.MINIMUM_TOKENS = self.rule.get_value("CD", "MIN_TOKENS")
        self.MIN_DUPLICATIONS = int(self.rule.get_value("CD", "MIN_DUPLICATIONS"))
        self.linegrabber = linegrabber

    def inspect(self):
        super().inspect()
        _duplications = self._find_all_duplications()

        for _dup in _duplications:
            _files = list(_dup["files"].keys())
            if len(_files) <= self.MIN_DUPLICATIONS:
                continue  # Skip if minimum of duplications not reached
            self.escalate()
            _start_line = _dup["files"][_files[0]]
            _end_line = _start_line + _dup["lines"] - 1
            _duplicated_code = self.linegrabber.get_lines(_files[0], start_line=_start_line, end_line=_end_line)

            self.note_violation(_dup["files"], None, _duplicated_code, None)

    def _find_all_duplications(self):
        _list = self.pmd.cpd_exe(self.MINIMUM_TOKENS)
        return self.pmd.cpd_to_dict(_list)
