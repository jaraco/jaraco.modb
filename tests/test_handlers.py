from __future__ import print_function

import importlib
import collections
import decimal

import six
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

class MyText(six.text_type):
	def __reduce__(self):
		return MyText, (six.text_type(self),)

class TestUnicodeSubclass(object):
	"This technique demonstrates how to handle a text-type subclass"
	@classmethod
	def setup_class(cls):
		jsonpickle.handlers.registry.register(MyText,
			jsonpickle.handlers.SimpleReduceHandler)

	def test_UnicodeSubclass(self):
		roundtrip(MyText('foo'))
