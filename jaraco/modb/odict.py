import collections

from . import handlers

@handlers.register
class OrderedDictHandler(handlers.SimpleReduceHandler):
    _handles = collections.OrderedDict,
