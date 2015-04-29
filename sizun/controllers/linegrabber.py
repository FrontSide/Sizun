
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from .externalexecutor import ExternalExecutor
from sizun.errorhandlers.concrete_error import LineNotFoundError


class LineGrabber:
    """
    Provides operations to catch lines from files
    by line numbers using the SED(1) cl-tool
    """

    SED_MAIN = "sed"
    OP_QUIET = "--quiet"
    SINGLE_LINE_CMD = "{}p"
    LINE_AREA_CMD = "{},{}p"  # From line to line

    def __init__(self, settings):
        self.settings = settings
        self.sourcepath = settings.get_sourcepath()

    def get_lines(self, filepath, start_line, end_line=None, absolute_path=False):

        if not absolute_path:
            full_path = self.sourcepath + "/" + filepath
        else:
            full_path = filepath

        if end_line:
            _cmd = self.LINE_AREA_CMD.format(start_line, end_line)
        else:
            _cmd = self.SINGLE_LINE_CMD.format(start_line)

        _openfile = open(full_path, "rb")
        _res = ExternalExecutor.exe([self.SED_MAIN, self.OP_QUIET, _cmd], instream=_openfile)
        _openfile.close()

        if len(_res) is 0:
            raise LineNotFoundError("No result for lines {}:{} in file {}".format(start_line, end_line, full_path))
        if len(_res) is 1:
            return _res[0]
        return _res
