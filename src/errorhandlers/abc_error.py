
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

from abc import ABCMeta

class ErrorABC(Exception, metaclass=ABCMeta):

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message=message
        if status_code is not None:
                self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['type'] = "error"
        rv['message'] = self.message
        return rv