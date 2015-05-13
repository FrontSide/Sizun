
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

from flask import Flask, request, jsonify, Response
from flask.ext.cors import CORS, cross_origin
from sizun.controllers.filehandler import FileHandler
from sizun.controllers.rulehandler import RuleHandler
from sizun.errorhandlers.concrete_error import InvalidRequestError,\
                                         ComprehensionError, \
                                         ExternalDependencyError, \
                                         NotFoundInConfigError
from sizun.controllers.confighandler import ConfigHandler
from sizun.controllers.settings import InspectionSettings
from sizun.controllers.inspectors.inspection import InspectionRunner
import logging

# Main Application
app = Flask(__name__)

# Log to file

app.logger.debug("START")

log_fh = logging.FileHandler("main.log")
log_fh.setLevel(logging.DEBUG)
app.logger.addHandler(log_fh)

app.logger.debug("OK")

# Configs
routch = ConfigHandler('config/routes.sizcon')
mainch = ConfigHandler('config/application.sizcon')
rulech = ConfigHandler('config/rules.sizcon')
inspsettings = InspectionSettings(mainch)
inspsettings.reset()
rulehandler = RuleHandler(rulech, inspsettings)
rulehandler.reset()
fh = FileHandler(inspsettings)

# Allow Cross Origin Resource Sharing on ALL ROUTES
cors = CORS(app)

# Load Routes from config file
r_home = routch.get("VIEW", "HOME")
r_set_srcpath = routch.get("SOURCEPATH", "SET")
r_get_srcpath = routch.get("SOURCEPATH", "GET")
r_get_srcpath_tree = routch.get("SOURCEPATH", "TREE")
r_activate_inspection = routch.get("INSPECTION", "ACTIVATE")
r_deactivate_inspection = routch.get("INSPECTION", "DEACTIVATE")
r_isset_inspection = routch.get("INSPECTION", "ISSET")
r_reset_rule = routch.get("RULE", "RESET")
r_change_rule = routch.get("RULE", "CHANGE")
r_get_rule = routch.get("RULE", "GET")
r_get_all_rules = routch.get("RULE", "ALL")
r_set_language = routch.get("LANGUAGE", "SET")
r_get_language = routch.get("LANGUAGE", "GET")
r_run_single = routch.get("RUN", "SINGLE")
r_run_full = routch.get("RUN", "FULL")

# Routing #


@app.route(r_home)
def home():
    """
    Root/Home Page - Shows the ReST API Paths
    """
    return jsonify(routch.getall())


@app.route('/sourcepath/set/<path:sourcepath>')
def set_srcpath(sourcepath):
    """
    Set the sourcepath where the inspection is conducted
    """
    inspsettings.set_sourcepath(sourcepath.strip("'"))
    return get_srcpath()


@app.route(r_get_srcpath)
def get_srcpath():
    """
    Get the sourcepath where the inspection is conducted
    """
    try:
        return jsonify({"SOURCEPATH": inspsettings.get_sourcepath()})
    except (ComprehensionError, InvalidRequestError) as error:
        return jsonify(error.to_dict()), error.status_code


@app.route(r_set_language)
def set_language(language):
    """
    Set the project's used language
    """
    inspsettings.set_language(language)
    return get_language()


@app.route(r_get_language)
def get_language():
    """
    Get the project's used language
    """
    try:
        return jsonify({"LANGUAGE": inspsettings.get_language()})
    except (ComprehensionError, InvalidRequestError) as error:
        return jsonify(error.to_dict()), error.status_code


@app.route(r_activate_inspection)
def activate_inspection(inspection_key):
    """
    Activates the given inspection/metric
    inspection_key: the key for the inspection as it is listed in
                    application.sizon config file under the "INSPECTION" category
    """
    inspsettings.activate_inspection(inspection_key)
    return isset_inspection(inspection_key)


@app.route(r_deactivate_inspection)
def deactivate_inspection(inspection_key):
    inspsettings.deactivate_inspection(inspection_key)
    return isset_inspection(inspection_key)


@app.route(r_isset_inspection)
def isset_inspection(inspection_key):
    try:
        return jsonify({"INSPECTION": {inspection_key: inspsettings.isset_inspection(inspection_key)}})
    except (InvalidRequestError) as error:
        return jsonify(error.to_dict()), error.status_code


@app.route(r_change_rule)
def set_rule(inspection_key, rule_key, value):
    """
    Changes the given rule of the given metric to the given value
    keys must be as in rules.sizon configfile
    """
    rulehandler.set_value(inspection_key, rule_key, value)
    return get_rule(inspection_key, rule_key)


@app.route(r_reset_rule)
def reset_rule(inspection_key, rule_key):
    rulehandler.reset_value(inspection_key, rule_key)
    return get_rule(inspection_key, rule_key)


@app.route(r_get_rule)
def get_rule(inspection_key, rule_key):
    try:
        return jsonify({"RULE": {inspection_key: {rule_key: rulehandler.get_value(inspection_key, rule_key)}}})
    except (InvalidRequestError) as error:
        return jsonify(error.to_dict()), error.status_code


@app.route(r_get_all_rules)
def get_all_rules():
    try:
        return jsonify(rulehandler.get_all_rules())
    except (InvalidRequestError) as error:
        return jsonify(error.to_dict()), error.status_code


@app.route(r_run_single)
def run_single_inspection(inspection_key):
    """
    Run one specific inspection and return results as json
    The "inspection_key" must accord to the key set in the
    application.sizon config file under the INSPECTION category
    """
    try:
        return jsonify(InspectionRunner(inspsettings, rulehandler).run(specific_inspection=inspection_key))
    except (ExternalDependencyError, InvalidRequestError) as error:
        return jsonify(error.to_dict()), error.status_code


@app.route(r_run_full)
def run_full_inspection():
    """
    Run full inspection-suit and return results as json
    """
    try:
        return jsonify(InspectionRunner(inspsettings, rulehandler).run())
    except (ExternalDependencyError, InvalidRequestError, NotFoundInConfigError) as error:
        return jsonify(error.to_dict()), error.status_code


@app.route(r_get_srcpath_tree)
def list_tree():
    """
    Get the directory tree from the sourcepath
    """
    try:
        return jsonify(fh.get_tree())
    except InvalidRequestError as error:
        return jsonify(error.to_dict()), error.status_code

# Run app
if __name__ == "__main__":
    app.run(port=8373, debug=True)
