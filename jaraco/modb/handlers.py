import jsonpickle.handlers

def register(handler_class, *handled_types):
    handled_types = handled_types or getattr(handler_class, '_handles', [])
    for handled_type in handled_types:
        jsonpickle.handlers.registry.register(handled_type, handler_class)
    return handler_class

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

    @classmethod
    def handles(cls, target):
        """
        Decorator for any class with a suitable __reduce__ method.
        """
        register(cls, target)
        return target
