"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""
from .confighandler import ConfigHandler
from .filehandler import FileHandler
from .externalexecutor import ExternalExecutor
import os
import re
from subprocess import Popen, PIPE
from flask import current_app as app


class PMDHandler():

    # PMD
    APPLICATION_PMD = "pmd"

    PMD_OP_OUTPUT = "-f"
    OUTPUT_TYPE = "csv"

    PMD_OP_RULESET = "-R"
    RULESET = "java-basic"

    PMD_OP_SOURCE_DIR = "-d"

    # CPD
    APPLICATION_CPD = "cpd"

    CPD_OP_SOURCE_DIR = "--files"

    CPD_OP_LANGUAGE = "--language"

    CPD_OP_OUTPUT = "--format"

    CPD_OP_MINIMUM_TOKENS = "--minimum-tokens"

    def __init__(self, _settings):
        self.settings = _settings
        self.fh = FileHandler(self.settings)
        self.language = _settings.get_language()
        self.sourcepath = _settings.get_sourcepath()
        self.MAIN_EXE = _settings.get_pmdexe()

    def pmd_exe(self):
        _out = ExternalExecutor.exe([self.MAIN_EXE,
                                    self.APPLICATION_PMD,
                                    self.PMD_OP_SOURCE_DIR,
                                    self.sourcepath,
                                    self.PMD_OP_OUTPUT,
                                    self.OUTPUT_TYPE,
                                    self.PMD_OP_RULESET,
                                    self.RULESET], resultdelimiter=",")

    def cpd_exe(self, minimum_tokens=50):
        return ExternalExecutor.exe([self.MAIN_EXE,
                                    self.APPLICATION_CPD,
                                    self.CPD_OP_SOURCE_DIR,
                                    self.sourcepath,
                                    self.CPD_OP_OUTPUT,
                                    self.OUTPUT_TYPE,
                                    self.CPD_OP_LANGUAGE,
                                    self.language,
                                    self.CPD_OP_MINIMUM_TOKENS,
                                    minimum_tokens], resultdelimiter=",")

    def cpd_to_dict(self, _lines):
        """
        Returns a list of dictionaries whereas each dict is
        one duplication issue. With keys:
        @lines for the number of lines of the duplicated code
        @tokens for the number of tokens of the duplicated code
        @occurrences for the numver of duplications of this issue
        @files >a dictionary< with all files as keys that accommodate this duplication
               and its start line number as value
        """
        _res = list()

        for l in _lines:
            _dup = dict()
            if _lines.index(l) is 0 or len(l) < 5:
                continue
            _dup["lines"] = l[0]
            _dup["tokens"] = l[1]
            _dup["occurences"] = l[2]
            _dup["files"] = dict()
            l_rest = l[3:]
            for i in range(0, len(l_rest)-1, 2):
                _filename = l_rest[i+1].rstrip("\n").replace(self.sourcepath + "/", "")
                _dup["files"][_filename] = l_rest[i]
            _res.append(_dup)
        app.logger.debug("cpd_to_dict :: {}".format(_res))
        return _res
