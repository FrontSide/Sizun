
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from sizun.controllers.filehandler import FileHandler
from sizun.errorhandlers.concrete_error import ComprehensionError, InvalidRequestError
import os


class InspectionSettingsMock:

    BASIC_SECTION_KEY = "BASIC"
    INSP_SECTION_KEY = "INSPECTION"
    SOURCEPATH_KEY = "SOURCEPATH"
    LANGUAGE_KEY = "LANGUAGE"
    TARGET_KEY = "TARGET"
    PMDEXE_KEY = "PMDEXE"

    def __init__(self):
        self.fh = FileHandler(self)
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
    language = "JAVA"

    def set_language(self, _language):
        self.language = _language

    def get_language(self):
        return self.language

    def set_sourcepath(self, _sourcepath):
        # unused _sourcepath
        return

    def get_sourcepath(self):
        return self.get_apppath()

    """
    Handles the target folder settings in the main config file
    This is the folder where temporary data that is created during
    execution is stored
    """
    targetfolder = ""

    def set_targetfolder(self, _targetfolder):
        self.targetfolder = _targetfolder

    def get_targetfolder(self):
        return self.targetfolder

    """
    Handels the path to the PMD executable
    """

    pmdexe = ""

    def get_pmdexe(self):
        return self.pmdexe

    """
    Handles whether a metric is enabled/disabled for inspection
    """
    def isset_inspection(self, _metricname):
        isset_dict = {
            "CC": True,
            "CD": True
        }
        return isset_dict[_metricname]
