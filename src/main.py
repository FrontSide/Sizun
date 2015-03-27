
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

from flask import Flask, request, jsonify
from controllers.filehandler import FileHandler
from errorhandlers.concrete_error import InvalidRequestError,\
                                         ComprehensionError, \
                                         ExternalDependencyError
from controllers.confighandler import ConfigHandler
from controllers.settings import InspectionSettings
from controllers.inspectors.inspection import InspectionRunner



"""
Main Application and Routing
"""
app = Flask(__name__)
routch = ConfigHandler('config/routes.sizcon')
mainch = ConfigHandler('config/application.sizcon')
inspsettings = InspectionSettings(mainch)
fh = FileHandler(inspsettings)


"""
Load Routes from config file
"""
r_home = routch.get("VIEW", "HOME")
r_set_srcpath = routch.get("SOURCEPATH", "SET")
r_get_srcpath_tree = routch.get("SOURCEPATH", "TREE")
r_get_language = routch.get("LANGUAGE", "GET")
r_run_full = routch.get("RUN", "FULL")


@app.route(r_home)
def home():
    """
    Home
    """
    return "Salute monde..."


@app.route(r_set_srcpath)
def set_srcpath(sourcepath):
    """
    Set the sourcepath where the inspection is conducted
    """
    inspsettings.set_sourcepath(sourcepath)
    return "OK"


@app.route(r_get_srcpath_tree)
def list_tree():
    """
    Get the directory tree from the sourcepath
    """
    try:
        return jsonify(fh.get_tree())
    except InvalidRequestError as error:
        return jsonify(error.to_dict()), error.status_code


@app.route(r_get_language)
def get_language():
    """
    Get the project's used language
    """
    try:
        return jsonify({"LANG": inspsettings.get_language()})
    except (ComprehensionError, InvalidRequestError) as error:
        return jsonify(error.to_dict()), error.status_code


@app.route(r_run_full)
def run_full_inspection():
    """
    Run full inspectionsuit and return results
    """
    try:
        return jsonify(InspectionRunner(inspsettings).run())
    except ExternalDependencyError as error:
        return jsonify(error.to_dict()), error.status_code


@app.route("/write")
def store():
    """
    Write to a file in the target ('results') folder
    """
    content = request.args.get('c')
    fh = Filehandler()
    fh.write_to_target("testfile", content)
    return "OK"

""" """
if __name__ == "__main__":
    app.run(debug=True)
