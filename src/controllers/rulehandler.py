"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from .confighandler import ConfigHandler


class RuleHandler:

    RULES_CONFIGFILE = "config/rules.sizcon"

    def __init__(self, _settings):
        # Instantiate a Configuration Handler fot the according syntax file
        self.language = _settings.get_language()
        self.app_path = _settings.get_apppath()
        self.confighandler = ConfigHandler("{}/{}".format(self.app_path, self.RULES_CONFIGFILE))

    def get_value(self, inspection_type, rulename):
        return self.confighandler.get(inspection_type, rulename)
