
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from .confighandler import ConfigHandler

class SyntaxHandler:

    SYNTAXFILES_FOLDER = "config/syntax/"
    SYNTAXFILES_APPDX = ".syn"

    ELEMENTS_SECTION = "ELEMENTS"

    def __init__(self, _settings):
        #Instantiate a Configuration Handler fot the according syntax file
        self.language = _settings.get_language()
        self.path_to_config = _settings.get_apppath()
        self.confighandler = ConfigHandler(self.path_to_config + "/" + self.SYNTAXFILES_FOLDER + self.language + self.SYNTAXFILES_APPDX)

    def get_if_regex(self):
        """
        Returns the regex by which if statments can be dedected
        in the specified language's sourcecode
        """
        return self.confighandler.get(self.ELEMENTS_SECTION, "IF")

    def get_method_regex(self):
        """
        Returns the regex by which method-starts can be dedected
        in the specified language's sourcecode
        """
        return self.confighandler.get(self.ELEMENTS_SECTION, "METHOD")
