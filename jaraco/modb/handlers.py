import jsonpickle.handlers

def register(class_):
    for handled_type in getattr(class_, '_handles', []):
        jsonpickle.handlers.registry.register(handled_type, class_)
    return class_

class SimpleReduceHandler(jsonpickle.handlers.BaseHandler):
    """
    Follow the __reduce__ protocol to pickle an object. As long as the factory
    and its arguments are pickleable, this should pickle any object that
    implements the reduce protocol.
    """
    def flatten(self, obj, data):
        pickler = self._base
        if not pickler.unpicklable:
            return unicode(obj)
        data['__reduce__'] = map(pickler.flatten, obj.__reduce__())
        return data

    def restore(self, obj):
        unpickler = self._base
        cls, args = map(unpickler.restore, obj['__reduce__'])
        return cls(*args)
