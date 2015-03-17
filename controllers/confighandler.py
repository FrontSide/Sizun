
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""
import configparser

class ConfigHandler:

    def __init__(self, path):
        self.path = path
        self.config = configparser.ConfigParser()

    def set(self, key, subkey, value):

        # Create section if not existent
        if not key in self.config.sections():
            self.config[key] = dict()

        self.config[key][subkey] = value

        with open(self.path, 'w') as configfile:
            self.config.write(configfile)

    def get(self, key, subkey):
        with open(self.path, 'r') as configfile:
            self.config.read_file(configfile)

        return self.config[key][subkey]
