
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

from flask import Flask, request, jsonify
from controllers.filehandler import FileHandler
from errorhandlers.concrete_error import InvalidRequestError, ComprehensionError
from controllers.confighandler import ConfigHandler
from controllers.settings import InspectionSettings



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

"""
Home
"""
@app.route(r_home)
def home():
    return "Salute monde..."



"""
Set the sourcepath where the inspection is conducted
"""
@app.route(r_set_srcpath)
def set_srcpath(sourcepath):
    inspsettings.set_sourcepath(sourcepath)
    return "OK"



"""
Get the directory tree from the sourcepath
"""
@app.route(r_get_srcpath_tree)
def list_tree():
    try:
        return jsonify(fh.get_tree())
    except InvalidRequestError as error:
        return jsonify(error.to_dict()), error.status_code



"""
Get the project's used language
"""
@app.route(r_get_language)
def get_language():
    try:
        return jsonify({"LANG" : inspsettings.get_language()})
    except (ComprehensionError, InvalidRequestError) as error:
        return jsonify(error.to_dict()), error.status_code



"""
Write to a file in the target ('results') folder
"""
@app.route("/write")
def store():
    content = request.args.get('c')
    fh = Filehandler()
    fh.write_to_target("testfile", content)
    return "OK"

""" """
if __name__ == "__main__":
    app.run(debug=True)
