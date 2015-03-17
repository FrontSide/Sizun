
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""

"""
Instantiates a parser accd. to the parameter
passed to the constructor
"""

class ParserFactory():

    concrete_parser = {'JAVA':JavaParser, 'PY':PyParser}

    def create(self, language):
        return self.concrete_parser[language]()
