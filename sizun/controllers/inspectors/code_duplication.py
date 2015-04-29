
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
        self.linegrabber = linegrabber

    def inspect(self):
        super().inspect()
        _duplications = self._find_all_duplications()

        for _dup in _duplications:
            self.escalate()
            _files = list(_dup["files"].keys())
            _occ_tupes = ["{} from line {}".format(k, v) for (k, v) in _dup["files"].items() if k is not _files[0]]
            _note = "Duplicated in :: {}".format(", ".join(_occ_tupes))
            self.note_violation(_files[0], _dup["files"][_files[0]], None, _note)
            _code_in_line = self.linegrabber.get_lines(_files[0], _dup["files"][_files[0]])
            app.logger.debug("Code from line {} in file {} is :: {}".format(_dup["files"][_files[0]], _files[0], _code_in_line))

    def _find_all_duplications(self):
        _list = self.pmd.cpd_exe(self.MINIMUM_TOKENS)
        return self.pmd.cpd_to_dict(_list)
