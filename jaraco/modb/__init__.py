import warnings

import jsonpickle.pickler
import jsonpickle.unpickler
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
	warnings.warn("It is no longer necessary to call jaraco.modb.init",
		DeprecationWarning)

def encode(value):
	return to_bson(jsonpickle.pickler.Pickler().flatten(value))

def decode(value):
	return jsonpickle.unpickler.Unpickler().restore(from_bson(value))
