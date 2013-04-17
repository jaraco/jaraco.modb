import sys
import collections

from . import handlers

@handlers.register
class OrderedDictHandler(handlers.SimpleReduceHandler):
    if sys.version_info > (2,7):
        _handles = collections.OrderedDict,
