
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from errorhandlers.concrete_error import ExternalDependencyError
from .inspection import InspectionABC
from controllers.agresulthelper import AGResultHelper


class CDInspector(InspectionABC):

    def __init__(self, pmdhandler, rulehandler):
        self.pmd = pmdhandler
        self.INSPECTION = "CD"
        self.rule = rulehandler
        self.MINIMUM_TOKENS = self.rule.get_value("CD", "MIN_TOKENS")

    def inspect(self):
        super().inspect()
        _duplications = self._find_all_duplications()

        for _dup in _duplications:
            self.escalate()
            _files = list(_dup["files"].keys())
            app.logger.debug("_dub :: {}".format(_files))
            _dup_files = _files[1:]
            app.logger.debug("_dub :: {}".format(_dup_files))
            _note = "Duplicated in :: {}".format(", ".join(_dup_files))
            self.note_violation(_files[0], _dup["files"][_files[0]], None, _note)

    def _find_all_duplications(self):
        _list = self.pmd.cpd_exe(self.MINIMUM_TOKENS)
        return self.pmd.cpd_to_dict(_list)
