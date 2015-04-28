
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from controllers.filehandler import FileHandler
from errorhandlers.concrete_error import ComprehensionError, InvalidRequestError
import os


class InspectionSettings:

    BASIC_SECTION_KEY = "BASIC"
    INSP_SECTION_KEY = "INSPECTION"
    SOURCEPATH_KEY = "SOURCEPATH"
    LANGUAGE_KEY = "LANGUAGE"
    TARGET_KEY = "TARGET"
    PMDEXE_KEY = "PMDEXE"

    def __init__(self, _config):
        self.fh = FileHandler(self)
        self.conf = _config
        self.apppath = os.getcwd()

    def reset(self):
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
        _language = self.conf.get(self.BASIC_SECTION_KEY, self.LANGUAGE_KEY)
        try:
            _language = self.conf.get(self.BASIC_SECTION_KEY, self.LANGUAGE_KEY)
        except NotFoundInConfigError:
            _language = None
        if _language is None:
            _language = self.fh.detect_language()

        self.set_language(_language)
        return _language

    def set_sourcepath(self, _sourcepath):
        """
        Handles the sourcepath settings in the main config file
        """
        self.conf.set(self.BASIC_SECTION_KEY, self.SOURCEPATH_KEY, _sourcepath)

    def get_sourcepath(self):
        try:
            return self.conf.get(self.BASIC_SECTION_KEY, self.SOURCEPATH_KEY)
        except NotFoundInConfigError:
            raise InvalidRequestError("No source path in config file found")

        return _sourcepath

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
