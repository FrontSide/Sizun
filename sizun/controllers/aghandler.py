
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""
from .confighandler import ConfigHandler
from .filehandler import FileHandler
from .externalexecutor import ExternalExecutor
from sizun.errorhandlers.concrete_error import WrongParametersError
from flask import current_app as app
import os


class AGHandler():

    C_MAIN = "ag"
    C_OP_FILES = "-G"

    def __init__(self, _settings):
        self.settings = _settings
        self.fh = FileHandler(self.settings)
        self.language = _settings.get_language()
        self.sourcepath = _settings.get_sourcepath()
        self.syntax = ConfigHandler("config/syntax/{}.syn".format(self.language))

    def source_exe(self, _keyword, file=None):
        """
        Looks for the >keyword<
            in all source files for the defined language if file=None
            in the given file is file!=None
        """

        # define which files to look for
        if file is None:
            _file_regex = "{}$".format(self.language)
        else:
            _file_regex = file

        os.chdir(self.sourcepath)
        _out = ExternalExecutor.exe([self.C_MAIN, _keyword, self.C_OP_FILES, _file_regex], resultdelimiter=":")
        os.chdir(self.settings.get_apppath())

        return _out

    def to_dict(self, _list, includecode=False):
        """
        Turns a list created by source_exe to a dictionary which has
        filenames as keys holding each one dict with line numbers as keys and the codeline as values
        if includecode is True

        { filename :
            { line : code,
              line : code }
        ,etc...}

        By default the code is not included, thus it returns a dictionary with the filenames as keys and
        lists of line numbers as values

        { filename :
            [line, line],
        etc...}

        """
        _res = dict()
        for el in _list:
            if includecode:
                if el[0] not in _res:
                    _res[el[0]] = dict()
                _res[el[0]][int(el[1])] = el[2].strip()
            else:
                if el[0] not in _res:
                    _res[el[0]] = list()
                _res[el[0]].append(int(el[1]))

        app.logger.debug("resulting dic is {}".format(_res))
        return _res


class AGResultHelper:
    """
    Offers a Library to manage the results
    coming from the AGHandler with static methods
    """

    def get_values_in_range(values, min_val=0, max_val=None):
        """
        Returns all values of tha list that are between min and max
        """
        if max_val is None:
            return [v for v in values if v > min_val]
        return [v for v in values if v > min_val and v < max_val]

    def get_lines_witin_sections(lines, section_starts):
        """
        Returns a dictionary with the line numbers of section starts as keys and
        lists of all line numbers that are within the according area as values

        example usage:
        a section_start could be defined by the start of a method
        All lines (as given in the 'lines varialbe')
        that are within the start of a method and the start of the next method
        are the values of this key (which is again the section start)
        """
        _lwa = dict()
        for sec in section_starts:
            try:
                next_section_start = section_starts[section_starts.index(sec)+1]
                lines_within = AGResultHelper.get_values_in_range(lines, sec, next_section_start)
            except IndexError:
                lines_within = AGResultHelper.get_values_in_range(lines, sec, None)
            _lwa[sec] = lines_within
        app.logger.debug("get_lines_witin_sections returns :: {}".format(_lwa))
        return _lwa

    def get_length_of_sections(section_starts):
        """
        Returns a dict with all section-start-linen-umbers as keys
        and the number of lines until the next section start as value
        """
        _los = dict()
        for sec in section_starts:
            try:
                _los[sec] = section_starts[section_starts.index(sec)+1] - sec
            except IndexError:
                _los[sec] = 777777  # TODO: Should be [length of file] - sec
        return _los

    def get_code(full_dict, filename, line_nr):
        """
        Returns the code for the related line in the given file
        taken from dict
        """
        try:
            return full_dict[filename][line_nr]
        except IndexError:
            _msg = "No code could be found for line {} in file \"{}\". \
                    Are you sure you passed a full dict?".format(line_nr, filename)
            app.logger.debug(_msg)
            raise WrongParametersError(str(_msg))

    def get_line_numbers(full_dict, filename):
        """
        Returns a list of the line numbers from a file taken from from a full dict
        """
        try:
            return sorted(list(full_dict[filename].keys()))
        except IndexError:
            _msg = "No lines could be found in file \"{}\". \
                    Are you sure you passed a full dict?".format(filename)
            app.logger.debug(_msg)
            raise WrongParametersError(str(_msg))
