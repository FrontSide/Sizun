
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from errorhandlers.concrete_error import ComprehensionError, InvalidRequestError
import logging
import os

"""
Handles the reading from directories and files
"""
class FileHandler:

    def __init__(self, _settings):
        self.tree = dict()
        self.settings = _settings

    #Directory for target files which safe the results
    target = "results"

    def get_tree(self):
        _srcpath = self.settings.get_sourcepath()
        try:
            self.tree = self.fetch_tree(_srcpath)
        except FileNotFoundError:
            raise InvalidRequestError("Sourcepath: '%s' seems to be invalid" % _srcpath)
        return self.tree

    """
    returns the tree for the given path
    and all its files and subdirectories recursively
    """
    def fetch_tree(self, path):

        current=os.listdir(path)

        tree = dict()

        for e in current:
            if os.path.isdir(path + "/" + e):
                tree[e] = self.fetch_tree(path + "/" + e)
            else:
                tree[e] = None

        return tree

    """
    Assumes the used language
    by looking for the most common file ending in the srcpath root
    """
    def detect_language(self):

        _file_endings = list()
        _tree = self.get_tree()

        for k in _tree:
            
            # Skip if directory
            # Files have None as value
            if _tree[k] is None:
                _file_endings.append(k.split('.')[-1])

        return max(set(_file_endings), key=_file_endings.count)

    """
    writes -content- to file -filename- in target directory
    optionally overwrites existing content of the file
    """
    def write_to_target(self, filename, content, overwrite=False):

        if not os.path.isdir(self.target):
            os.makedirs(self.target)

        if overwrite or not os.path.isfile(self.target + "/" + filename):
            f = open(self.target + "/" + filename, 'w')
        else:
            f = open(self.target + "/" + filename, 'a')

        f.write(content)
        f.close()
        return
