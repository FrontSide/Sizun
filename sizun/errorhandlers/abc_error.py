
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

from abc import ABCMeta


class ErrorABC(Exception, metaclass=ABCMeta):

    def throw(self, concrete_error, message, status_code=None, payload=None):
        super(concrete_error, self).__init__(message)
        self.message = message
        self.concrete_error = concrete_error
        if status_code is not None:
                self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict()
        rv['type'] = "error"
        rv['message'] = self.message
        rv['error'] = "dfsf" # self.concrete_error
        return rv
