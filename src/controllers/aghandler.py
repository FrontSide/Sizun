
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""
from .confighandler import ConfigHandler
from errorhandlers.concrete_error import ExternalDependencyError
import os
import subprocess
from flask import current_app as app

class AGHandler():

    C_MAIN="ag"
    C_OP_FILES="-G"

    def __init__(self, _settings):
        self.settings = _settings
        self.fh = FileHandler(self.settings)
        self.language = _settings.get_language()
        self.sourcepath = _settings.get_sourcepath()
        self.targetfolder = _settings.get_targetfolder()
        self.syntax = ConfigHandler("config/syntax/%s.syn" % self.language)

    """
    Looks for the >keyword< in all source files for the defined language
    and writes the result in the >target< file in the /target folder
    """
    def source_exe(self, _keyword, _target):
        #> {}/{}/{}.out , self.settings.get_apppath(), self.targetfolder, _target
        exe_string = "{} {} {} [.]*.{}".format(self.C_MAIN, _keyword, self.C_OP_FILES, self.language)
        app.logger.debug("ag commad to execute is {}".format(exe_string))
        try:

            os.chdir(self.sourcepath)

            # run ag
            p = subprocess.Popen(exe_string, stdout=subprocess.PIPE)
            output = p.stdout.read()

            # write result to file
            self.fh.write_to_target(_target, output, overwrite=True)

            os.chdir(self.settings.get_apppath())

        except FileNotFoundError:
            raise ExternalDependencyError("Could not find 'ag' installation.")
            
        return
