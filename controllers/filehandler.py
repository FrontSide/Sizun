
"""
Sizun
MIT License
(C) 2015 David Rieger
"""
from flask import current_app as app
import logging
import os

"""
Handles the reading from directories and files
"""
class Filehandler:

    #Directory for target files which safe the results
    target = "results"

    """
    returns the tree for the given path
    and all its files and subdirectories recursively
    """
    def get_tree(self, path):

        tree=dict()


        current=os.listdir(path)

        for e in current:
            if os.path.isdir(path + "/" + e):
                tree[e] = self.get_tree(path + "/" + e)

            else:
                tree[e] = None

        return tree

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
