
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

from flask import Flask, request, jsonify
from controllers.filehandler import Filehandler
from errorhandlers.concrete_error import InvalidRequestError, ComprehensionError
from controllers.confighandler import ConfigHandler

"""
Main Application and Routing
"""

app = Flask(__name__)
mainch = ConfigHandler('config/sizun.conf')
fh = Filehandler(mainch)

"""
Home
"""
@app.route("/")
def home():
    return "Salute monde..."

"""
Set the sourcepath where the inspection is conducted
"""
@app.route("/sourcepath/set/<path:p>")
def set_srcpath(p):
    mainch.set("DEFAULT", "SOURCEPATH", p)
    return "OK"

"""
Get the directory tree from the sourcepath
"""
@app.route("/sourcepath/tree/get")
def list_tree():
    try:
        return jsonify(fh.get_tree())
    except FileNotFoundError:
        ive = InvalidRequestError("'" + fh.srcpath + "' is not a valid path")
        return jsonify(ive.to_dict()), ive.status_code

"""
Get the project's used language
"""
@app.route("/language/get")
def get_language():
    try:
        return jsonify({"LANG" : fh.get_language()})
    except ComprehensionError as error:
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
