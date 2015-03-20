
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from errorhandlers.concrete_error import ExternalDependencyError
import os
from .inspection import InspectionABC

class CCInspector(InspectionABC):

    def __init__(self, filehandler):
        self.fh = filehandler
        return

    def run(self):
        super().run(self.fh)
        self._exe_ag()
        result = dict()
        result["insp"] = "done"
        return result


    def _exe_ag(self):
        #try:
        p = os.system("ag if")
        #except FileNotFoundError:
        #    raise ExternalDependencyError("Could not find 'ag' installation.")
        #return
