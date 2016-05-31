SortedCollections
=================

.. image:: https://api.travis-ci.org/grantjenks/sortedcollections.svg
    :target: http://www.grantjenks.com/docs/sortedcollections/

`SortedCollections`_ is an Apache2 licensed Python sorted collections library.

Features
--------

- Pure-Python
- Depends on the `SortedContainers
  <http://www.grantjenks.com/docs/sortedcontainers/>`_ module.
- ValueSortedDict - Dictionary with (key, value) item pairs sorted by value.
- ItemSortedDict - Dictionary with key-function support for item pairs.
- OrderedDict - Ordered dictionary with numeric indexing support.
- OrderedSet - Ordered set with numeric indexing support.
- IndexableDict - Dictionary with numeric indexing support.
- IndexableSet - Set with numeric indexing support.
- SegmentList - List with fast random access insertion and deletion.
- 100% code coverage testing.

Quickstart
----------

Installing `SortedCollections`_ is simple with `pip
<http://www.pip-installer.org/>`_::

    $ pip install sortedcollections

You can access documentation in the interpreter with Python's built-in help
function:

::

    >>> from sortedcollections import ValueSortedDict
    >>> help(ValueSortedDict)

Recipes
-------

- `Value Sorted Dictionary Recipe`_
- `Item Sorted Dictionary Recipe`_
- `Ordered Dictionary Recipe`_
- `Ordered Set Recipe`_
- `Indexable Dictionary Recipe`_
- `Indexable Set Recipe`_
- `Segment List Recipe`_

.. _`Value Sorted Dictionary Recipe`: http://www.grantjenks.com/docs/sortedcollections/valuesorteddict.html
.. _`Item Sorted Dictionary Recipe`: http://www.grantjenks.com/docs/sortedcollections/itemsorteddict.html
.. _`Ordered Dictionary Recipe`: http://www.grantjenks.com/docs/sortedcollections/ordereddict.html
.. _`Ordered Set Recipe`: http://www.grantjenks.com/docs/sortedcollections/orderedset.html
.. _`Indexable Dictionary Recipe`: http://www.grantjenks.com/docs/sortedcollections/indexabledict.html
.. _`Indexable Set Recipe`: http://www.grantjenks.com/docs/sortedcollections/indexableset.html
.. _`Segment List Recipe`: http://www.grantjenks.com/docs/sortedcollections/segmentlist.html

Reference and Indices
---------------------

- `SortedCollections Documentation`_
- `SortedCollections at PyPI`_
- `SortedCollections at Github`_
- `SortedCollections Issue Tracker`_

.. _`SortedCollections Documentation`: http://www.grantjenks.com/docs/sortedcollections/
.. _`SortedCollections API Reference`: http://www.grantjenks.com/docs/sortedcollections/api.html
.. _`SortedCollections at PyPI`: https://pypi.python.org/pypi/sortedcollections
.. _`SortedCollections at Github`: https://github.com/grantjenks/sortedcollections
.. _`SortedCollections Issue Tracker`: https://github.com/grantjenks/sortedcollections/issues

SortedCollections License
-------------------------

Copyright 2015-2016 Grant Jenks

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

.. _`SortedCollections`: http://www.grantjenks.com/docs/sortedcollections/
