===========
jaraco.modb
===========

.. contents::

Overview
--------

``jaraco.modb`` is a small, pure-Python library for persisting Python
objects to `MongoDB <http://www.mongodb.org/>`_.

``jaraco.modb`` is written by Jason R. Coombs.  It is licensed under an
`MIT-style permissive license
<http://www.opensource.org/licenses/mit-license.php>`_.

You can install it with ``easy_install jaraco.modb`` or grab the source
code from the `mercurial repository
<http://bitbucket.org/jaraco/jaraco.modb>`_.

Manual Usage
------------

``jaraco.modb`` facilitates using `jsonpickle` to produce MongoDB-friendly
representations of pickleable Python objects for easy storage in a MongoDB
database.

One may simply encode and decode Python objects to MongoDB
BSON-friendly representations::

    class MyObject(object):
        def __init__(self, val):
            self.val = val

    import jaraco.modb
    import pymongo
    mongo_collection = pymongo.Connection().mydb.mycollection
    val = MyObject(3)
    # save the object to the DB
    id = mongo_collection.save(jaraco.modb.encode(val))
    # retrieve the object from the DB
    new_val = jaraco.modb.decode(mongo_collection.find_one(id))
    assert isinstance(new_val, MyObject)
    assert new_val.val == 3

A more detailed tutorial is now `published as an iPython Notebook
<http://nbviewer.ipython.org/urls/bitbucket.org/jaraco/jaraco.modb/raw/tip/tutorial.ipynb?create=1>`_.


Automatic Usage
---------------

``jaraco.modb`` also provides an SON Manipulator suitable for automatically
encoding arbitrary objects for a pymongo.Database::

    jaraco.modb.SONManipulator.install(mongo_collection.database)
    mongo_collection.save({'val': val})

Unfortunately, due to a limitation with the API of the SONManipulator,
it's not possible to save a custom object as the document itself (the
document must always be a dict).
