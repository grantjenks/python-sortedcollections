SortedCollections
=================

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

.. toctree::

   valuesorteddict
   itemsorteddict
   ordereddict
   orderedset
   indexabledict
   indexableset
   segmentlist

Reference and Indices
---------------------

- `SortedCollections Documentation`_
- `SortedCollections at PyPI`_
- `SortedCollections at Github`_
- `SortedCollections Issue Tracker`_
- :ref:`SortedCollections Index <genindex>`
- :ref:`Search SortedCollections Documentation <search>`

.. _`SortedCollections Documentation`: http://www.grantjenks.com/docs/sortedcollections/
.. _`SortedCollections at PyPI`: https://pypi.python.org/pypi/sortedcollections
.. _`SortedCollections at Github`: https://github.com/grantjenks/sortedcollections
.. _`SortedCollections Issue Tracker`: https://github.com/grantjenks/sortedcollections/issues

SortedCollections License
-------------------------

.. include:: ../LICENSE

.. _`SortedCollections`: http://www.grantjenks.com/docs/sortedcollections/
