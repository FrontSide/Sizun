
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from abc import ABCMeta
from controllers.filehandler import FileHandler
from flask import current_app as app

class InspectionRunner:

    def __init__(self, config):
        self.config=config

    """
    Run the full inspection suite
    """
    def run(self):

        result = dict()

        # Start only inspections that are enabled in config file
        # Cyclomatic Complexity
        if self.config.isset("INSPECTION", "CC"):
            from .circular_complexity import CCInspector
            result["cc"] = CCInspector(FileHandler(self.config)).run()

        return result


"""
Abstract Inspection Super-Class
"""
class InspectionABC(metaclass=ABCMeta):

    def run(self, filehandler):
        """ Triggers the inspection process """
        app.logger.debug("An inspection has been triggered...")
        return
