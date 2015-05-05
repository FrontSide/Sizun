
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from abc import ABCMeta
from sizun.errorhandlers.concrete_error import ComprehensionError, InvalidRequestError
import logging
import os


class FileHandler:
    """
    Handles the reading from directories and files
    """

    def __init__(self, _settings):
        self.tree = dict()
        self.settings = _settings

    def get_tree(self):
        _srcpath = self.settings.get_sourcepath()
        try:
            self.tree = self.fetch_tree(_srcpath)
        except FileNotFoundError:
            raise InvalidRequestError("Sourcepath: '%s' seems to be invalid" % _srcpath)
        return self.tree

    def fetch_tree(self, path):
        """
        returns the tree for the given path
        and all its files and subdirectories recursively
        """

        current = os.listdir(path)

        tree = dict()

        for e in current:
            if os.path.isdir(path + "/" + e):
                tree[e] = self.fetch_tree(path + "/" + e)
            else:
                tree[e] = None

        return tree
