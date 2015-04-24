
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""
from .confighandler import ConfigHandler
from .filehandler import FileHandler
from errorhandlers.concrete_error import ExternalDependencyError, ExternalExecutionError
import os
from subprocess import Popen, PIPE
from flask import current_app as app


class AGHandler():

    C_MAIN = "ag"
    C_OP_FILES = "-G"

    def __init__(self, _settings):
        self.settings = _settings
        self.fh = FileHandler(self.settings)
        self.language = _settings.get_language()
        self.sourcepath = _settings.get_sourcepath()
        self.targetfolder = _settings.get_targetfolder()
        self.syntax = ConfigHandler("config/syntax/{}.syn".format(self.language))

    def source_exe(self, _keyword, file=None):
        """
        Looks for the >keyword<
            in all source files for the defined language if file=None
            in the given file is file!=None
        """

        # define which files to look for
        if file is None:
            _search_regex = "{}$".format(self.language)

        else:
            _search_regex = file

        try:
            os.chdir(self.sourcepath)
            # The next command runs silver searcher ag and pipes stdout (binary) to _boutput
            # Form e.g. "ag if --java"
            _agproc = Popen([self.C_MAIN, _keyword, self.C_OP_FILES, _search_regex], stdout=PIPE, stderr=PIPE)

            os.chdir(self.settings.get_apppath())

        except FileNotFoundError:
            raise ExternalDependencyError("Could not find 'ag' installation.")

        _boutput = _agproc.stdout

        if _agproc.returncode is not (0 or None):
            raise ExternalExecutionError("'ag' failed to execute", returncode=_agproc.returncode,
                                         stderr=_agproc.stderr.read().decode("utf-8"),
                                         stdout=_boutput.read().decode("utf-8"))

        # List comprehsnion to decode the byte lines coming from the ag call
        _lines = [l.decode("utf-8").split(":") for l in _boutput.readlines()]

        return _lines

    def to_simple_dic(self, _list):
        """
        Turns a list created by source_exe to a dictionary which has
        filenames as keys and lists of line numbers as values
        """
        _res = dict()
        for el in _list:
            if el[0] not in _res:
                _res[el[0]] = list()
            _res[el[0]].append(int(el[1]))
            _res[el[0]].sort()

        app.logger.debug("resulting dic is {}".format(_res))
        return _res

    def to_full_dic(self, _list):
        """
        Turns a list created by source_exe to a dictionary which has
        filenames as keys and lists of dicts wirh line numbers and the codeline as values
        """
        _res = dict()
        for el in _list:
            if el[0] not in _res:
                _res[el[0]] = list()
            _entry = dict()
            _entry["line"] = int(el[1])
            _entry["code"] = el[2].strip()
            _res[el[0]].append(_entry)

        app.logger.debug("resulting dic is {}".format(_res))
        return _res
