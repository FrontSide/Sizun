
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

from abc import ABCMeta

class ParserABC(metaclass=ABCMeta):

    @abstractmethod
    def get_methods():
        """ Returns all methods of the class """
        return

    @abstractmethod
    def get_tree():
        """ Returns the parsed tree of a class """
        return
