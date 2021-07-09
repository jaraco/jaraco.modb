import datetime as dt

import jsonpickle.pickler
import jsonpickle.unpickler

# override the default pickler/unpickler to better handle some types


class Pickler(jsonpickle.pickler.Pickler):
    def _flatten(self, obj):
        if isinstance(obj, dt.datetime) and not obj.utcoffset():
            # naive datetimes or UTC datetimes can be stored directly
            return obj
        if isinstance(obj, bytes):
            return obj
        return super(Pickler, self)._flatten(obj)


class Unpickler(jsonpickle.unpickler.Unpickler):
    pass


def encode(value):
    return Pickler().flatten(value)


def decode(value):
    return Unpickler().restore(value)
