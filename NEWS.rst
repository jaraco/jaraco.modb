v6.1.0
======

Features
--------

- Require Python 3.8 or later.


v6.0.0
======

Removed SONManipulator.

v5.0.0
======

Dropped support for unpickling bson.Binary objects.
Use 4.x to restore objects that may contain those objects
and then re-save them as bytes.

v4.1.0
======

Refreshed package metadata.

4.0
===

Switch to `pkgutil namespace technique
<https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages>`_
for the ``jaraco`` namespace.

3.6
===

* Bump to jsonpickle 0.9.5+ for integrated reduce support.

3.5.1
=====

* Refreshed package.
* Pinned jsonpickle due to jsonpickle #200.

3.5
===

* Moved hosting to Github.

3.4
===

* Bump jsonpickle to 0.9.2.

3.3.2
=====

* Pin to jsonpickle 0.7.2, as 0.8 and 0.9.1 cause tests to fail.

3.3.1
=====

* Regenerate project packaging metadata.

3.3
===

* Bump jsonpickle requirement to 0.6.2 final (or later).

3.2
===

* Replace ``jaraco.util`` dependency with ``jaraco.text``.

3.1
===

* Add an SONManipulator according to the `MongoDB example
  <http://api.mongodb.org/python/current/examples/custom_type.html>`_.

3.0
===

* Update to work with jsonpickle 0.6.
* Add support for Python 3.
* Removed ``jaraco.modb.handlers``.

2.1.1
=====

* Workaround for `IndexError in jsonpickle
  <https://github.com/jsonpickle/jsonpickle/issues/37>`_.

2.1
===

* Added convenience method for decorating functions with the
  ``SimpleReduceHandler``.

2.0
===

* Removed initializer function (`jaraco.modb.init()`). Clients should remove
  that call (if present) before upgrading to 2.0.

1.2
===

* Now store naive and UTC datetimes naturally in MongoDB.
* The encoder/decoder now subclasses the `jsonpickle` classes to more
  efficiently handle binary strings.

1.1
===

* Added proper support for datetime objects.
* Added support for OrderedDictionaries.

1.0.4
=====

* Removed requirement to call `jaraco.modb.init()` to initialize.

1.0
===

* Initial release
