
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from .confighandler import ConfigHandler


class SyntaxHandler:

    SYNTAXFILES_FOLDER = "config/syntax/"
    SYNTAXFILES_APPDX = ".syn"

    ELEMENTS_SECTION = "ELEMENTS"

    def __init__(self, _settings):
        # Instantiate a Configuration Handler fot the according syntax file
        self.language = _settings.get_language()
        self.app_path = _settings.get_apppath()
        self.confighandler = ConfigHandler("{}/{}{}{}".format(
                    self.app_path,
                    self.SYNTAXFILES_FOLDER,
                    self.language,
                    self.SYNTAXFILES_APPDX))

    def get_flowpath_regex(self):
        """
        Returns the regex by which if statments can be dedected
        in the specified language's sourcecode
        """
        return self.confighandler.get(self.ELEMENTS_SECTION, "FLOWPATH")

    def get_method_regex(self):
        """
        Returns the regex by which method-starts can be dedected
        in the specified language's sourcecode
        """
        return self.confighandler.get(self.ELEMENTS_SECTION, "METHOD")

    def get_foreign_reference_regex(self):
        """
        Returns the regex by which foreign references can be dedected
        in the specified language's sourcecode
        """
        return self.confighandler.get(self.ELEMENTS_SECTION, "FOREIGN_REFERENCE")
