from __future__ import print_function

import importlib
import collections
import decimal

import pytest
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

class MyUnicode(six.text_type):
	def __reduce__(self):
		return MyUnicode, (six.text_type(self),)

@pytest.mark.skipif(six.PY3, reason="Python 2 only")
class TestUnicodeSubclass(object):
	"This technique demonstrates how to handle a Unicode subclass"
	@classmethod
	def setup_class(cls):
		jsonpickle.handlers.registry.register(MyUnicode,
			jsonpickle.handlers.SimpleReduceHandler)

	def test_UnicodeSubclass(self):
		roundtrip(MyUnicode('foo'))
