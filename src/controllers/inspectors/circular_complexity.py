
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from errorhandlers.concrete_error import ExternalDependencyError
from .inspection import InspectionABC

class CCInspector(InspectionABC):

    def __init__(self, aghandler):
        self.ag=aghandler
        self.INSPECTION = "CC"

    def run(self):

        super().run()

        # Trigger AG
        self.exe_ag("if[\\W]*[\(]", "cc")
        return self.result

    def exe_ag(self, _keyword, _filename):
        self.ag.source_exe(_keyword, _filename)
        return
