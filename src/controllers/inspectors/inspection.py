
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from abc import ABCMeta, abstractmethod
from controllers.filehandler import FileHandler
from controllers.aghandler import AGHandler
from flask import current_app as app

class InspectionRunner:

    def __init__(self, _settings):
        self.settings=_settings
        self.ag=AGHandler(self.settings)

    """
    Run the full inspection suite
    """
    def run(self):

        result = dict()

        # Start only inspections that are enabled in config file
        # Cyclomatic Complexity
        if self.settings.isset_inspection("CC"):
            from .circular_complexity import CCInspector
            result["CC"] = CCInspector(self.ag).run()

        return result


"""
Abstract Inspection Super-Class
"""
class InspectionABC(metaclass=ABCMeta):

    def run(self):
        """ Triggers the inspection process """
        app.logger.debug("An inspection has been triggered...")

        # Write dict entry for JSON response
        self.result = dict()
        self.result["insp"] = "done"

        return self.result

    @abstractmethod
    def exe_ag(_keyword, _filename):
        """ Trrigers the AG Handler """
        return
