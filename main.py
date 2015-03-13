"""
Sizun - Software Quality Inspection
"""

from flask import Flask, request
from controllers.filehandler.fetcher import Fetcher
app = Flask(__name__)

""" """

@app.route("/")
def home():
    return "Salute monde..."

@app.route("/list/tree")
def list_tree():
    path = request.args.get('p')
    if path is None:
        return "No Path Given"
    else:
        fetcher = Fetcher()
        return fetcher.get_tree(path)


""" """

if __name__ == "__main__":
    app.run(debug=True)
