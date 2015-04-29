"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

from subprocess import Popen, PIPE
from flask import current_app as app


class ExternalExecutor():

    def exe(commandlist, resultdelimiter=None, instream=None):
        """
        Executes an external executable witht the
        command and parameters given in commandlist

        Returns a list of all lines from stdout
        """

        app.logger.debug("command is :: {}".format(" ".join(commandlist)))

        try:
            _proc = Popen(commandlist, stdout=PIPE, stderr=PIPE, stdin=instream)
        except FileNotFoundError:
            raise ExternalDependencyError("Executable \"{}\" not found. Is it installed?".format(commandlist[0]))

        if _proc.returncode is not (0 or None):
            raise ExternalExecutionError("Failed to execute \"{}\"".format(" ".join(commandlist)),
                                         returncode=_agproc.returncode,
                                         stderr=_agproc.stderr.read().decode("utf-8"))

        _boutput = _proc.stdout

        if resultdelimiter:
            return [l.decode("utf-8").split(resultdelimiter) for l in _boutput.readlines()]
        else:
            return [l.decode("utf-8").rstrip("\n").strip() for l in _boutput.readlines()]
