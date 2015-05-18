
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

import os
import shutil
from flask import current_app as app
from .externalexecutor import ExternalExecutor


class GitHandler():

    BASE_PATH = "gittmp"

    C_MAIN = "git"
    C_CLONE = "clone"

    def __init__(self, settings):
        self.settings = settings

    def clone_repo(self, url):
        """
        Clones a public git repository to the local git base path
        """
        shutil.rmtree(self.BASE_PATH)
        os.mkdir(self.BASE_PATH)
        os.chdir(self.BASE_PATH)
        ExternalExecutor.exe([self.C_MAIN, self.C_CLONE, url])
        os.chdir(self.settings.get_apppath())

    def get_path_to_repo(self):
        """
        Returns the path to the root of the last cloned git repo
        """
        try:
            repo_folder = os.listdir(self.BASE_PATH)[0]
        except IndexError:
            return None

        return "{}/{}/{}".format(self.settings.get_apppath(), self.BASE_PATH, repo_folder)
