from __future__ import print_function

import importlib
import collections
import decimal

import jsonpickle

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

# This technique demonstrates how to handle a Unicode subclass
@jsonpickle._handlers.SimpleReduceHandler.handles
class MyUnicode(unicode):
	def __reduce__(self):
		return MyUnicode, (unicode(self),)

def test_UnicodeSubclass():
	roundtrip(MyUnicode('foo'))

def test_custom_handler_references():
	"""
	https://github.com/jsonpickle/jsonpickle/issues/37
	"""
	ob = MyUnicode('test me')
	subject = dict(a=ob, b=ob, c=ob)
	roundtrip(subject)
