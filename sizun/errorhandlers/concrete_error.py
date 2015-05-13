
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""
from flask import jsonify, current_app as app
from .abc_error import ErrorABC


class InvalidRequestError(ErrorABC):

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().throw(InvalidRequestError, message)


class NotFoundInConfigError(ErrorABC):

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().throw(NotFoundInConfigError, "There is something missing in a config file :: {}".format(message))


class LineNotFoundError(ErrorABC):

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().throw(LineNotFoundError, message)


class ComprehensionError(ErrorABC):

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().throw(ComprehensionError, message)


class UnallowedOperationError(ErrorABC):

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().throw(UnallowedOperationError, message)


class WrongParametersError(ErrorABC):

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().throw(WrongParametersError, message)


class ExternalDependencyError(ErrorABC):

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().throw(ExternalDependencyError, message)


class ExternalExecutionError(ErrorABC):

    status_code = 500

    def __init__(self, message, status_code=None, payload=None, returncode=None, stderr=None, stdout=None):
        super().throw(ExternalExecutionError, message)
        app.logger.error("returncode :: {}".format(returncode))
        app.logger.error("STDERR :: {}".format(stderr))
