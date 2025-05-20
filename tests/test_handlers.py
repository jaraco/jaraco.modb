from __future__ import annotations

import collections
import decimal
import importlib

import jsonpickle


def setup_module() -> None:
    importlib.import_module('jaraco.modb')


def roundtrip(ob: object) -> None:
    encoded = jsonpickle.encode(ob)
    print('encoded is', encoded)
    decoded = jsonpickle.decode(encoded)
    assert decoded == ob


def test_OrderedDict() -> None:
    d = collections.OrderedDict(y=3)
    roundtrip(d)


def test_Decimal() -> None:
    roundtrip(decimal.Decimal(1.0))
    roundtrip(decimal.Decimal(1000))


class MyText(str):
    def __reduce__(self) -> tuple[type[MyText], tuple[str]]:
        return MyText, (str(self),)


class TestUnicodeSubclass:
    "This technique demonstrates how to handle a text-type subclass"

    def test_UnicodeSubclass(self) -> None:
        roundtrip(MyText('foo'))
