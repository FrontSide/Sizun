
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from .filehandler import FileHandler
from sizun.errorhandlers.concrete_error import ComprehensionError, InvalidRequestError, NotFoundInConfigError
from .confighandler import ConfigHandler
import os
from flask import current_app as app


class InspectionSettings:

    BASIC_SECTION_KEY = "BASIC"
    INSP_SECTION_KEY = "INSPECTION"
    SOURCEPATH_KEY = "SOURCEPATH"
    LANGUAGE_KEY = "LANGUAGE"
    TARGET_KEY = "TARGET"
    PMDEXE_KEY = "PMDEXE"

    PATH_TO_DEF_CONFIG = "config/application.sizcon.default"

    def __init__(self, _config):
        self.fh = FileHandler(self)
        self.conf = _config
        self.apppath = os.getcwd()

    def reset(self):
        """
        Load all from default settings
        """
        # app.logger.debug("Reset Inspection Config")
        ch_old = ConfigHandler(self.conf.path)
        ch_new = ConfigHandler(self.PATH_TO_DEF_CONFIG)
        ConfigHandler.setall(old=ch_old, new=ch_new)
        return

    def get_apppath(self):
        """
        Returns the path where sizun was initially startet from
        (not stored in config file because mustn't be manually manipulated)
        """
        return self.apppath

    def set_language(self, _language):
        self.conf.set(self.BASIC_SECTION_KEY, self.LANGUAGE_KEY, _language)

    def get_language(self):
        _language = self.conf.get(self.BASIC_SECTION_KEY, self.LANGUAGE_KEY)
        try:
            _language = self.conf.get(self.BASIC_SECTION_KEY, self.LANGUAGE_KEY)
        except NotFoundInConfigError:
            _language = None
        if _language is None:
            _language = self._detect_language()

        self.set_language(_language)
        return _language

    def _detect_language(self):
        """
        Detects the used language
        by looking for the most common file ending in the root folder of the srcpath tree
        """

        _file_endings = list()
        _tree = self.fh.get_tree()

        for k in _tree:

            # Files have None as value, skip directories
            if _tree[k] is None:
                _file_endings.append(k.split('.')[-1])

        return max(set(_file_endings), key=_file_endings.count)

    def set_sourcepath(self, _sourcepath):
        if _sourcepath[0] is not '/':
            _sourcepath = '/' + _sourcepath
        self.conf.set(self.BASIC_SECTION_KEY, self.SOURCEPATH_KEY, _sourcepath)

    def get_sourcepath(self):
        try:
            return self.conf.get(self.BASIC_SECTION_KEY, self.SOURCEPATH_KEY)
        except NotFoundInConfigError:
            raise InvalidRequestError("No source path in config file found")

        return _sourcepath

    def get_pmdexe(self):
        """
        Path to PMD executable
        """
        try:
            return self.conf.get(self.BASIC_SECTION_KEY, self.PMDEXE_KEY)
        except NotFoundInConfigError:
            raise InvalidRequestError("Failed to find execution path for PMD")

    def isset_inspection(self, _metricname):
        return self.conf.isset(self.INSP_SECTION_KEY, _metricname)

    def activate_inspection(self, _metricname):
        self.conf.set(self.INSP_SECTION_KEY, _metricname, "true")

    def deactivate_inspection(self, _metricname):
        self.conf.set(self.INSP_SECTION_KEY, _metricname, "false")
