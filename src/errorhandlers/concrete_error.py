
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""
from flask import jsonify
from errorhandlers.abc_error import ErrorABC

class InvalidRequestError(ErrorABC):

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)

class ComprehensionError(ErrorABC):

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)

class ExternalDependencyError(ErrorABC):

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
