"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from .confighandler import ConfigHandler


class RuleHandler:

    RULES_DEFAULTS_CONFIGFILE = "config/rules.sizcon.default"

    def __init__(self, _confighandler, _settings):
        # Instantiate a Configuration Handler fot the according syntax file
        self.language = _settings.get_language()
        self.app_path = _settings.get_apppath()
        self.confighandler = _confighandler
        self.defaults = ConfigHandler("{}/{}".format(self.app_path, self.RULES_DEFAULTS_CONFIGFILE))

    def get_value(self, inspection_type, rulename):
        return self.confighandler.get(inspection_type, rulename)

    def set_value(self, inspection_type, rulename, value):
        self.confighandler.set(inspection_type, rulename, value)

    def reset_value(self, inspection_type, rulename):
        default_value = self.defaults.get(inspection_type, rulename)
        self.set_value(inspection_type, rulename, default_value)

    def get_all_rules(self):
        return self.confighandler.getall()
