
from flask import current_app as app
from json import JSONEncoder
from enum import Enum


class EnumEncoder(JSONEncoder):

    def encode(self, o):
        app.logger.debug("entered custom enum encoder")
        if isinstance(o, Dict):
            app.logger.debug("enum detected :: {}".format(o.name))
            return {"__enum__": str(o.name)}
        return JSONEncoder.default(self, o)


def as_enum(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(globals()[name], member)
    else:
        return d
