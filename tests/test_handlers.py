import collections
import decimal
import importlib

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
    roundtrip(decimal.Decimal('1.0'))
    roundtrip(decimal.Decimal(1000))


class MyText(str):
    def __reduce__(self):
        return MyText, (str(self),)


class TestUnicodeSubclass:
    "This technique demonstrates how to handle a text-type subclass"

    def test_UnicodeSubclass(self):
        roundtrip(MyText('foo'))
