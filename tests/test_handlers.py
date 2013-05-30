from __future__ import print_function

import importlib
import collections
import decimal

import jsonpickle

import jaraco.modb.handlers

def setup_module():
	importlib.import_module('jaraco.modb')

def roundtrip(ob):
	encoded = jsonpickle.encode(ob)
	print('encoded is', encoded)
	decoded = jsonpickle.decode(encoded)
	assert decoded == ob

def test_OrderedDict():
	d = collections.OrderedDict(y=3)
	roundtrip(d)

def test_Decimal():
	roundtrip(decimal.Decimal(1.0))
	roundtrip(decimal.Decimal(1000))

@jaraco.modb.handlers.SimpleReduceHandler.handles
class MyUnicode(unicode):
	def __reduce__(self):
		return MyUnicode, (unicode(self),)

def test_UnicodeSubclass():
	roundtrip(MyUnicode('foo'))
