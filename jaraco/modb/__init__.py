from __future__ import absolute_import

import datetime as dt

import jsonpickle.pickler
import jsonpickle.unpickler
import bson.binary
from jaraco.util.string import is_binary

# load the specialized handlers
__import__('jaraco.modb.datetime')
__import__('jaraco.modb.odict')

# override the default pickler/unpickler to handle binary strings
class Pickler(jsonpickle.pickler.Pickler):
	def flatten(self, obj):
		if isinstance(obj, dt.datetime) and not obj.utcoffset():
			# naive datetimes or UTC datetimes can be stored directly
			return obj
		flattened = super(Pickler, self).flatten(obj)
		if is_binary(flattened):
			return bson.binary.Binary(flattened)
		return flattened

class Unpickler(jsonpickle.unpickler.Unpickler):
	def restore(self, obj):
		restored = super(Unpickler, self).restore(obj)
		if isinstance(restored, bson.binary.Binary):
			return bytes(restored)
		return restored

def encode(value):
	return Pickler().flatten(value)

def decode(value):
	return Unpickler().restore(value)
