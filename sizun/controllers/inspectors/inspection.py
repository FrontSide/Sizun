
"""
Sizun
MIT License
(C) 2015 David Rieger
"""

from abc import ABCMeta
from enum import IntEnum, unique
from sizun.controllers.aghandler import AGHandler
from sizun.controllers.pmdhandler import PMDHandler
from sizun.controllers.syntaxhandler import SyntaxHandler
from sizun.controllers.linegrabber import LineGrabber
from sizun.errorhandlers.concrete_error import UnallowedOperationError
from flask import current_app as app


class InspectionRunner:

    inspection_set = ["CC", "CD", "FE", "LPL", "MC"]

    def __init__(self, _settings, _rulehandler):
        self.settings = _settings
        self.ag = AGHandler(self.settings)
        self.syntaxhandler = SyntaxHandler(self.settings)
        self.rulehandler = _rulehandler
        self.pmd = PMDHandler(self.settings)
        self.linegrabber = LineGrabber(self.settings)

    def run(self, specific_inspection=None):
        """
        Run the full inspection suite
        """
        result = dict()
        stat = dict()

        # Get the activation status of all inspection suits OR
        # deactivate all inspections except the one set in specific_inspection, respectively
        if specific_inspection is None:
            for insp in self.inspection_set:
                stat[insp] = self.settings.isset_inspection(insp)
        else:
            for insp in self.inspection_set:
                if specific_inspection.upper() == insp:
                    stat[insp] = True
                else:
                    stat[insp] = False

        # Run activated inspections
        # Cyclomatic Complexity
        if stat["CC"]:
            from .circular_complexity import CCInspector
            result["CC"] = CCInspector(self.ag, self.syntaxhandler, self.rulehandler).run()

        # Code Duplication
        if stat["CD"]:
            from .code_duplication import CDInspector
            result["CD"] = CDInspector(self.pmd, self.rulehandler, self.linegrabber).run()

        # Feature Envy
        if stat["FE"]:
            from .feature_envy import FEInspector
            result["FE"] = FEInspector(self.ag, self.syntaxhandler, self.rulehandler).run()

        # Long Parameter List
        if stat["LPL"]:
            from .long_parameter_list import LPLInspector
            result["LPL"] = LPLInspector(self.ag, self.syntaxhandler, self.rulehandler).run()

        # Message Chain
        if stat["MC"]:
            from .message_chain import MCInspector
            result["MC"] = MCInspector(self.ag, self.syntaxhandler, self.rulehandler).run()

        return result


class InspectionABC(metaclass=ABCMeta):
    """
    Abstract Inspection Super-Class
    """

    _result = dict()

    def run(self):
        """
        Triggers the inspection process
        and returns the resulting dictionary
        THIS IS THE METHOD THAT MUST BE CALLED FROM THE
        INSPECTION RUNNER
        """
        self.inspect()
        return self._result

    def inspect(self):
        """
        Main inspection process method
        Must be overridden by the concrete
        inspector subclass and must call this super method
        i.e. super().inspect()
        ! DO NOT ! DIRECTLY CALL THIS METHOD FROM THE INSPECTION RUNNER
        """
        app.logger.debug("An inspection has been triggered...")

        # Write dict entry for JSON response
        self._result = dict()
        self._result[str(ResultKey.ESCALATION)] = EscalationLevel.NO_ERROR
        self._result[str(ResultKey.VIOLATIONS)] = list()

    def note_violation(self, filename, line, code=None, info=None):
        """
        Adds the info of a rule violation to the result dictionary
        """
        violation = {"FILE": filename, "LINE": line, "CODE": code, "INFO": info}
        self._result[str(ResultKey.VIOLATIONS)].append(violation)

    def add_info(self, key, value):
        """
        Adds a key value pair to the result dictionary
        Called by the conrete inspector subclass whenever
        additional information needs to be provided
        """
        if key in ResultKey.__members__.items():
            raise UnallowedOperationError("Concrete Inspectors may not change the pre-defined key \"{}\"".format(key))
        self._result[str(key)] = value

    def escalate(self):
        """
        Ecalates the error level for the inspected metric
        Must be called from the concrete inspector subclass
        whenever a rule violation occurs and an escalation to
        a higher error level is necessary
        """

        _ecalation_level = self._result[str(ResultKey.ESCALATION)]

        if _ecalation_level is EscalationLevel.NO_ERROR:
            _ecalation_level = EscalationLevel.MINOR_ERROR

        elif _ecalation_level is EscalationLevel.MINOR_ERROR:
            _ecalation_level = EscalationLevel.MAJOR_ERROR

        else:
            _ecalation_level = EscalationLevel.CRITICAL_ERROR

        self._result[str(ResultKey.ESCALATION)] = _ecalation_level


class ResultKey(IntEnum):
    ESCALATION = 0
    VIOLATIONS = 1

    def __str__(self):
        return self.name


@unique
class EscalationLevel(IntEnum):

    NO_RESULT = 0
    NO_ERROR = 1
    MINOR_ERROR = 2
    MAJOR_ERROR = 3
    CRITICAL_ERROR = 4

    def __str__(self):
        return self.name
