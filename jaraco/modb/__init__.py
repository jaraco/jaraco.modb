import jsonpickle

# set up a couple of "serialization" functions for jsonpickle to produce
#  and consume JSON-ready dicts, rather than serializing to strings.
dumps = loads = lambda x: x

def init():
	jsonpickle.load_backend(__name__, 'dumps', 'loads', ValueError)
	jsonpickle.set_preferred_backend(__name__)

encode = jsonpickle.encode
decode = jsonpickle.decode
