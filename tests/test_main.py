import bson.binary
import py.test

import jaraco.modb

def test_to_bson():
	sample = dict(
		a = u'a string',
		b = 'another string',
		c = 'some binary bytes\x00\xff',
	)
	res = jaraco.modb.to_bson(sample)
	assert res['a'] == sample['a']
	assert res['b'] == sample['b']
	assert isinstance(res['c'], bson.binary.Binary)

class TestObject(object):
	def __init__(self, val):
		self.val = val

def test_object():
	ob = TestObject(1)
	serialized = jaraco.modb.encode(ob)
	ob_res = jaraco.modb.decode(serialized)
	assert isinstance(ob_res, TestObject)
	assert ob_res is not ob
	assert ob.val == ob_res.val

def test_nested_object():
	ob_nested = TestObject('child')
	ob_parent = TestObject(ob_nested)
	serialized = jaraco.modb.encode(ob_parent)
	restored = jaraco.modb.decode(serialized)
	assert isinstance(restored, TestObject)
	assert isinstance(restored.val, TestObject)
	assert restored.val.val == 'child'

class MyDict(dict):
	pass

def test_encode_dict_subclass():
	d = MyDict(a=3, b=4)
	encoded = jaraco.modb.encode(d)
	assert 'MyDict' in str(encoded)
	decoded = jaraco.modb.decode(encoded)
	assert isinstance(decoded, MyDict)

def test_init():
	"Init should do nothing, not cause errors"
	jaraco.modb.init()

def test_ordered_dict():
	try:
		import collections
		ob = collections.OrderedDict(a=1, c=3, b=4)
	except Exception:
		py.test.skip("OrderedDict not available")
	serialized = jaraco.modb.encode(ob)
	restored = jaraco.modb.decode(serialized)
	assert isinstance(restored, collections.OrderedDict)
	assert restored.keys() == list('acb')
	assert restored.values() == [1, 3, 4]
