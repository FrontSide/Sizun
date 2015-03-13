
"""
Sizun
"""

from flask import jsonify
from flask import current_app as app
import logging
import os

class Fetcher:

    def get_tree(self, path, raw=False):

        tree=dict()
        current=os.listdir(path)
        for e in current:
            if os.path.isdir(path + "/" + e):
                app.logger.debug('%s is a directory', path + "/" + e)
                tree[e] = self.get_tree(path + "/" + e, raw=True)

            else:
                app.logger.debug('%s is NOT a directory', path + "/" + e)
                tree[e] = None

        if raw is True:
            return tree
        return jsonify(tree)
