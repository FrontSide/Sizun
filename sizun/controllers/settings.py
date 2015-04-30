
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
        self.CHANGED_SOURCEPATH = True

    def reset(self):
        """
        Load all from default settings
        """
        # app.logger.debug("Reset Inspection Config")
        ch_old = ConfigHandler(self.conf.path)
        ch_new = ConfigHandler(self.PATH_TO_DEF_CONFIG)
        ConfigHandler.setall(old=ch_old, new=ch_new)
        return

    """
    Returns the path where sizun was initially startet from
    (not stored in config file because mustn't be manually manipulated)
    """
    def get_apppath(self):
        return self.apppath

    """
    Handles the language settings in the main config file
    """
    def set_language(self, _language):
        self.conf.set(self.BASIC_SECTION_KEY, self.LANGUAGE_KEY, _language)

    def get_language(self):
        try:
            _language = self.conf.get(self.BASIC_SECTION_KEY, self.LANGUAGE_KEY)
        except NotFoundInConfigError:
            _language = None

        if _language is None or self.CHANGED_SOURCEPATH is True:
            _language = self.fh.detect_language()
            self.CHANGED_SOURCEPATH = False

        self.set_language(_language)
        return _language

    def set_sourcepath(self, _sourcepath):
        """
        Handles the sourcepath settings in the main config file
        """
        self.conf.set(self.BASIC_SECTION_KEY, self.SOURCEPATH_KEY, _sourcepath)
        self.notice_sourcepath_changed()

    def get_sourcepath(self):
        try:
            return self.conf.get(self.BASIC_SECTION_KEY, self.SOURCEPATH_KEY)
        except NotFoundInConfigError:
            raise InvalidRequestError("No source path in config file found")

        return _sourcepath

    def notice_sourcepath_changed(self):
        """
        Set flag that sourcepath has been changed
        """
        self.CHANGED_SOURCEPATH = True

    """
    Handles the target folder settings in the main config file
    This is the folder where temporary data that is created during
    execution is stored
    """
    def set_targetfolder(self, _targetfolder):
        self.conf.set(self.BASIC_SECTION_KEY, self.TARGET_KEY, _targetfolder)

    def get_targetfolder(self):
        try:
            return self.conf.get(self.BASIC_SECTION_KEY, self.TARGET_KEY)
        except NotFoundInConfigError:
            raise InvalidRequestError("No target folder path in config file found")

    """
    Handels the path to the PMD executable
    """
    def get_pmdexe(self):
        try:
            return self.conf.get(self.BASIC_SECTION_KEY, self.PMDEXE_KEY)
        except NotFoundInConfigError:
            raise InvalidRequestError("Failed to find execution path for PMD")

    """
    Handles whether a metric is enabled/disabled for inspection
    """
    def isset_inspection(self, _metricname):
        return self.conf.isset(self.INSP_SECTION_KEY, _metricname)
