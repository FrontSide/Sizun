
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from errorhandlers.concrete_error import ExternalDependencyError
from .inspection import InspectionABC

class CCInspector(InspectionABC):

    # Folder for cc results in the target folder
    OUT_FOLDER = "cc/"

    def __init__(self, aghandler, syntaxhandler):
        self.ag=aghandler
        self.INSPECTION = "CC"
        self.syntax = syntaxhandler

    def run(self):
        super().run()

        #Find all "if"s and write them to if.out
        self._find_all_if()

        """ TODO: Get files where there are if's """
        """       Find method start in each file """
        """       Measure number of if's between
                  method starts (and end of
                  file resp.)                    """ 

        return self.result

    """ """


    def _find_all_if(self):
        return self.ag.source_exe(self.syntax.get_if_regex(), self.OUT_FOLDER + "if")

    def _find_method_start(self, _path):
        """
        Returns all line numbers of a file (=_path) where a new method is starting
        """
        return self.ag.source_exe(self.syntax.get_method_regex(), self.OUT_FOLDER + "if")
