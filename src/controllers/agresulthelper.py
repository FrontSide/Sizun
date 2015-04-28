
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

from flask import current_app as app
from errorhandlers.concrete_error import WrongParametersError


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
        All lines that are within the start of a method and the start of the next method
        are the values of this key (which is again the section start)
        """
        app.logger.debug("get_lines_witin_sections called with lines :: {} and section starts :: {}".format(lines, section_starts))
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
