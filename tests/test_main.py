import datetime
import collections

import bson.tz_util

import jaraco.modb


def test_to_bson():
    sample = dict(
        a='a string',
        b='another string'.encode('ascii'),
        c='some binary bytes'.encode('ascii') + b'\x00\xff',
    )
    res = jaraco.modb.encode(sample)
    assert res['a'] == sample['a']
    assert res['b'] == sample['b']
    assert jaraco.modb.decode(res) == sample


class ObjectUnderTest(object):
    def __init__(self, val):
        self.val = val


def test_object():
    ob = ObjectUnderTest(1)
    serialized = jaraco.modb.encode(ob)
    ob_res = jaraco.modb.decode(serialized)
    assert isinstance(ob_res, ObjectUnderTest)
    assert ob_res is not ob
    assert ob.val == ob_res.val


def test_nested_object():
    ob_nested = ObjectUnderTest('child')
    ob_parent = ObjectUnderTest(ob_nested)
    serialized = jaraco.modb.encode(ob_parent)
    restored = jaraco.modb.decode(serialized)
    assert isinstance(restored, ObjectUnderTest)
    assert isinstance(restored.val, ObjectUnderTest)
    assert restored.val.val == 'child'


class MyDict(dict):
    pass


def test_encode_dict_subclass():
    d = MyDict(a=3, b=4)
    encoded = jaraco.modb.encode(d)
    assert 'MyDict' in str(encoded)
    decoded = jaraco.modb.decode(encoded)
    assert isinstance(decoded, MyDict)


def test_ordered_dict():
    items = ('a', 1), ('c', 3), ('b', 4)
    ob = collections.OrderedDict(items)
    serialized = jaraco.modb.encode(ob)
    restored = jaraco.modb.decode(serialized)
    assert isinstance(restored, collections.OrderedDict)
    assert list(restored.keys()) == list('acb')
    assert list(restored.values()) == [1, 3, 4]


def test_datetime_naive():
    now = datetime.datetime.now()
    serialized = jaraco.modb.encode(now)
    assert isinstance(serialized, datetime.datetime)
    restored = jaraco.modb.decode(serialized)
    assert restored == now


def test_datetime_utc():
    now = datetime.datetime.now(bson.tz_util.utc)
    serialized = jaraco.modb.encode(now)
    assert isinstance(serialized, datetime.datetime)
    restored = jaraco.modb.decode(serialized)
    assert restored == now


def test_datetime_local():
    est = bson.tz_util.FixedOffset(-60 * 5, 'EST')
    now = datetime.datetime.now(est)
    serialized = jaraco.modb.encode(now)
    assert not isinstance(serialized, datetime.datetime)
    restored = jaraco.modb.decode(serialized)
    assert restored == now
