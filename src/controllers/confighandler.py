
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

    """
    Sets a value to a given key
    """
    def set(self, key, subkey, value):

        # Create section if not existent
        if key not in self.config.sections():
            self.config[key] = dict()

        self.config[key][subkey] = value

        with open(self.path, 'w') as configfile:
            self.config.write(configfile)

    """
    Returns the set value of a given key
    """
    def get(self, key, subkey):
        with open(self.path, 'r') as configfile:
            self.config.read_file(configfile)

        try:
            return self.config[key][subkey]
        except KeyError:
            return None

    """
    Returns the set boolean value of a given key
    """
    def isset(self, key, subkey):

        with open(self.path, 'r') as configfile:
            self.config.read_file(configfile)

        try:
            return self.config.getboolean(key, subkey)
        except KeyError:
            return False
