
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from controllers.filehandler import FileHandler
from errorhandlers.concrete_error import ComprehensionError, InvalidRequestError

class InspectionSettings:

    section_key = "INSPECTION"
    sourcepath_key = "SOURCEPATH"
    language_key = "LANGUAGE"

    def __init__(self, _config):
        self.fh=FileHandler(self)
        self.conf=_config

    """
    Handles the language settings in the main config file
    """
    def set_language(self, _language):
        self.conf.set(self.section_key, self.language_key, _language)

    def get_language(self):
        _language=self.conf.get(self.section_key, self.language_key)
        if not _language:
            try:
                _language = self.fh.detect_language()
            except ValueError:
                raise ComprehensionError("Could not find src files in source path root")

        self.set_language(_language)
        return _language


    """
    Handles the sourcepath settings in the main config file
    """
    def set_sourcepath(self, _sourcepath):
        self.conf.set(self.section_key, self.sourcepath_key, _sourcepath)

    def get_sourcepath(self):
        _sourcepath=self.conf.get(self.section_key, self.sourcepath_key)
        if not _sourcepath:
            raise InvalidRequestError("No source path in config file found")

        return _sourcepath
