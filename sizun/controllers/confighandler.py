
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""
import configparser
from sizun.errorhandlers.concrete_error import NotFoundInConfigError
from flask import current_app as app


class ConfigHandler:

    def __init__(self, path):
        self.path = path
        self.config = configparser.ConfigParser()

    def set(self, key, subkey, value):
        """
        Sets a value to a given key
        """
        with open(self.path, 'r') as configfile:
            self.config.read_file(configfile)

        # Create section if not existent
        if key not in self.config.sections():
            self.config[key] = dict()

        self.config[key][subkey] = value

        with open(self.path, 'w') as configfile:
            self.config.write(configfile)

    def get(self, key, subkey):
        """
        Returns the set value of a given key
        """
        with open(self.path, 'r') as configfile:
            self.config.read_file(configfile)

        try:
            return self.config[key][subkey]
        except KeyError:
            raise NotFoundInConfigError("file:: {}, key:: {}, subkey:: {}".format(self.path, key, subkey))

    def isset(self, key, subkey):
        """
        Returns the set boolean value of a given key
        """
        with open(self.path, 'r') as configfile:
            self.config.read_file(configfile)

        try:
            return self.config.getboolean(key, subkey)
        except KeyError:
            raise NotFoundInConfigError("file:: {}, key:: {}, subkey:: {}".format(self.path, key, subkey))

    def setall(old, new):
        """
        STATIC
        Overwrites all settings from file behind
        ConfigHandler old with those from file behind ConfigHandler new
        """
        with open(new.path, 'r') as configfile:
            # Read setting from new file into new confighandler
            new.config.read_file(configfile)

        with open(old.path, 'w') as configfile:
            # Write setting from new file/confighandler into old confighandler/file
            new.config.write(configfile)

    def getall(self):
        """
        Returns a list of all section with its subsections and their values as nested dict
        """
        with open(self.path, 'r') as configfile:
            self.config.read_file(configfile)

        res = dict()
        for section in self.config.sections():
            res[section] = dict()
            for rule, val in self.config[section].items():
                res[section][rule] = val
        return res
