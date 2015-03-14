
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

from flask import Flask, request, jsonify
from controllers.filehandler import Filehandler

"""
Main Application and Routing
"""

app = Flask(__name__)

@app.route("/")
def home():
    return "Salute monde..."

@app.route("/list/tree")
def list_tree():
    path = request.args.get('p')
    fh = Filehandler()
    return jsonify(fh.get_tree(path))

@app.route("/write")
def store():
    content = request.args.get('c')
    fh = Filehandler()
    fh.write_to_target("testfile", content)
    return "OK"



""""""
if __name__ == "__main__":
    app.run(debug=True)
