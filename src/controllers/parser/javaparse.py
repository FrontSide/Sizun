
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

from abc_parse import ParserABC
from plyj.parser import Parser as plyj

class JavaParser(ParserABC):

    @ParserABC.get_tree():
