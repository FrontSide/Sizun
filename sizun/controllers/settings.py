
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

    def get_language(self, enforce_detection=False):

        try:
            _language = self.conf.get(self.BASIC_SECTION_KEY, self.LANGUAGE_KEY)
        except NotFoundInConfigError:
            _language = None

        if enforce_detection or _language is None:
            _language = self._detect_language(self.fh.get_tree())
            self.set_language(_language)

        return _language

    def _detect_language(self, dir_tree):
        """
        Detects the used language
        by recursively looking for the most common file ending in the srcpath tree
        """

        _file_endings = list()

        for k, v in dir_tree.items():

            # Files have None as value, skip directories
            if v is None:
                _file_endings.append(k.split('.')[-1])
            # Recursively detect language in subdirectory tree
            else:
                _file_endings.append(self._detect_language(v))

        if len(_file_endings) is 0:
            return None

        return max(set(_file_endings), key=_file_endings.count)

    def set_sourcepath(self, _sourcepath):
        if _sourcepath[0] is not '/':
            _sourcepath = '/' + _sourcepath
        self.conf.set(self.BASIC_SECTION_KEY, self.SOURCEPATH_KEY, _sourcepath)

    def get_sourcepath(self, update_language=True):
        try:
            _sorucepath = self.conf.get(self.BASIC_SECTION_KEY, self.SOURCEPATH_KEY)
            if update_language:
                self.get_language(enforce_detection=True)
            return _sorucepath
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
