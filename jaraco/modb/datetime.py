from __future__ import absolute_import

import datetime

import jsonpickle.handlers
import jsonpickle.util

from . import handlers

# hack to disable REPR for datetime objects in jsonpickle 0.4.0:
jsonpickle.util.NEEDS_REPR = ()


@handlers.register
class DatetimeHandler(jsonpickle.handlers.BaseHandler):
    """
    Datetime objects use __reduce__, and they generate binary strings encoding
    the payload. This handler encodes that payload to reconstruct the
    object.
    """
    _handles = datetime.datetime, datetime.date, datetime.time
    def flatten(self, obj, data):
        pickler = self._base
        if not pickler.unpicklable:
            return unicode(obj)
        cls, args = obj.__reduce__()
        args = [args[0].encode('base64')] + map(pickler.flatten, args[1:])
        data['__reduce__'] = (pickler.flatten(cls), args)
        return data

    def restore(self, obj):
        cls, args = obj['__reduce__']
        value = args[0].decode('base64')
        unpickler = self._base
        cls = unpickler.restore(cls)
        params = map(unpickler.restore, args[1:])
        params = (value,) + tuple(params)
        return cls.__new__(cls, *params)

@handlers.register
class TimeDeltaHandler(handlers.SimpleReduceHandler):
    _handles = datetime.timedelta,
