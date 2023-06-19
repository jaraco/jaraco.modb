.. image:: https://img.shields.io/pypi/v/jaraco.modb.svg
   :target: https://pypi.org/project/jaraco.modb

.. image:: https://img.shields.io/pypi/pyversions/jaraco.modb.svg

.. image:: https://github.com/jaraco/jaraco.modb/workflows/tests/badge.svg
   :target: https://github.com/jaraco/jaraco.modb/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. .. image:: https://readthedocs.org/projects/PROJECT_RTD/badge/?version=latest
..    :target: https://PROJECT_RTD.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2023-informational
   :target: https://blog.jaraco.com/skeleton


``jaraco.modb`` is a small, pure-Python library for persisting Python
objects to `MongoDB <https://www.mongodb.org/>`_.

Manual Usage
============

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
    mongo_collection = pymongo.MongoClient().mydb.mycollection
    val = MyObject(3)
    # save the object to the DB
    id = mongo_collection.save(jaraco.modb.encode(val))
    # retrieve the object from the DB
    new_val = jaraco.modb.decode(mongo_collection.find_one(id))
    assert isinstance(new_val, MyObject)
    assert new_val.val == 3

A more detailed tutorial is now `published as a Jupyter Notebook
<https://nbviewer.jupyter.org/github/jaraco/jaraco.modb/blob/master/tutorial.ipynb>`_.


Automatic Usage
===============

``jaraco.modb`` also provides an SON Manipulator suitable for automatically
encoding arbitrary objects for a pymongo.Database::

    jaraco.modb.SONManipulator.install(mongo_collection.database)
    mongo_collection.save({'val': val})

Unfortunately, due to a limitation with the API of the SONManipulator,
it's not possible to save a custom object as the document itself (the
document must always be a dict).
