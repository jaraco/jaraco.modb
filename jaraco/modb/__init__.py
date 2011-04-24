import jsonpickle
import pymongo.binary
import jaraco.util.dictlib
from jaraco.util.string import is_binary

# set up a couple of "serialization" functions for jsonpickle to produce
#  and consume BSON-ready dicts, rather than serializing to strings.
def to_bson(json):
	# all this just so we can convert 'bytes' objects to pymongo Binary
	if isinstance(json, dict):
		return jaraco.util.dictlib.dict_map(to_bson, json)
	if isinstance(json, list):
		return map(to_bson, json)
	if is_binary(json):
		return pymongo.binary.Binary(json)
	return json

def from_bson(json):
	# all this just so we can convert pymongo Binary back to 'bytes'
	if isinstance(json, dict):
		return jaraco.util.dictlib.dict_map(from_bson, json)
	if isinstance(json, list):
		return map(from_bson, json)
	if isinstance(json, pymongo.binary.Binary):
		return bytes(json)
	return json

def init():
	# remove all other backends so only this one is used
	map(jsonpickle.remove_backend, jsonpickle.json._backend_names)
	jsonpickle.load_backend(__name__, 'to_bson', 'from_bson', ValueError)
	jsonpickle.set_preferred_backend(__name__)

encode = jsonpickle.encode
decode = jsonpickle.decode
