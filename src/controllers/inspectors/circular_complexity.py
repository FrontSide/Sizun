
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from .inspection import InspectionABC

class CCInspector(InspectionABC):

    def __init__(self):
        return

    def run(self, filehandler):
        super().run(filehandler)
        result = dict()
        result["insp"] = "done"
        return result
