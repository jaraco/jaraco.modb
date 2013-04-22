import importlib
import collections
import decimal

import jsonpickle

def setup_module():
	importlib.import_module('jaraco.modb')

def roundtrip(ob):
	encoded = jsonpickle.encode(ob)
	decoded = jsonpickle.decode(encoded)
	assert decoded == ob

def test_OrderedDict():
	d = collections.OrderedDict(y=3)
	roundtrip(d)

def test_Decimal():
	roundtrip(decimal.Decimal(1.0))
	roundtrip(decimal.Decimal(1000))
