import pymongo.binary
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
	assert isinstance(res['c'], pymongo.binary.Binary)

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
