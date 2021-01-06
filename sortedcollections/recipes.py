"""Sorted collections recipes implementations.

"""

from copy import deepcopy
from itertools import count
from sortedcontainers import SortedKeyList, SortedDict, SortedSet
from sortedcontainers.sortedlist import recursive_repr

###############################################################################
# BEGIN Python 2/3 Shims
###############################################################################

try:
    from collections import abc
except ImportError:
    import collections as abc

###############################################################################
# END Python 2/3 Shims
###############################################################################


class IndexableDict(SortedDict):
    """Dictionary that supports numerical indexing.

    Keys are numerically indexable using dict views. For example::

        >>> indexable_dict = IndexableDict.fromkeys('abcde')
        >>> keys = indexable_dict.keys()
        >>> sorted(keys[:]) == ['a', 'b', 'c', 'd', 'e']
        True

    The dict views support the sequence abstract base class.

    """
    def __init__(self, *args, **kwargs):
        super(IndexableDict, self).__init__(hash, *args, **kwargs)


class IndexableSet(SortedSet):
    """Set that supports numerical indexing.

    Values are numerically indexable. For example::

        >>> indexable_set = IndexableSet('abcde')
        >>> sorted(indexable_set[:]) == ['a', 'b', 'c', 'd', 'e']
        True

    `IndexableSet` implements the sequence abstract base class.

    """
    # pylint: disable=too-many-ancestors
    def __init__(self, *args, **kwargs):
        super(IndexableSet, self).__init__(*args, key=hash, **kwargs)

    def __reduce__(self):
        return self.__class__, (set(self),)


class ItemSortedDict(SortedDict):
    """Sorted dictionary with key-function support for item pairs.

    Requires key function callable specified as the first argument. The
    callable must accept two arguments, key and value, and return a value used
    to determine the sort order. For example::

        def multiply(key, value):
            return key * value
        mapping = ItemSortedDict(multiply, [(3, 2), (4, 1), (2, 5)])
        list(mapping) == [4, 3, 2]

    Above, the key/value item pairs are ordered by ``key * value`` according to
    the callable given as the first argument.

    """
    def __init__(self, *args, **kwargs):
        assert args and callable(args[0])
        args = list(args)
        func = self._func = args[0]
        def key_func(key):
            "Apply key function to (key, value) item pair."
            return func(key, self[key])
        args[0] = key_func
        super(ItemSortedDict, self).__init__(*args, **kwargs)

    def __delitem__(self, key):
        "``del mapping[key]``"
        if key not in self:
            raise KeyError(key)
        self._list_remove(key)
        dict.__delitem__(self, key)

    def __setitem__(self, key, value):
        "``mapping[key] = value``"
        if key in self:
            self._list_remove(key)
            dict.__delitem__(self, key)
        dict.__setitem__(self, key, value)
        self._list_add(key)

    _setitem = __setitem__

    def copy(self):
        "Return shallow copy of the mapping."
        return self.__class__(self._func, iter(self.items()))

    __copy__ = copy

    def __deepcopy__(self, memo):
        items = (deepcopy(item, memo) for item in self.items())
        return self.__class__(self._func, items)


class ValueSortedDict(SortedDict):
    """Sorted dictionary that maintains (key, value) item pairs sorted by value.

    - ``ValueSortedDict()`` -> new empty dictionary.

    - ``ValueSortedDict(mapping)`` -> new dictionary initialized from a mapping
      object's (key, value) pairs.

    - ``ValueSortedDict(iterable)`` -> new dictionary initialized as if via::

        d = ValueSortedDict()
        for k, v in iterable:
            d[k] = v

    - ``ValueSortedDict(**kwargs)`` -> new dictionary initialized with the
      name=value pairs in the keyword argument list.  For example::

        ValueSortedDict(one=1, two=2)

    An optional key function callable may be specified as the first
    argument. When so, the callable will be applied to the value of each item
    pair to determine the comparable for sort order as with Python's builtin
    ``sorted`` function.

    """
    def __init__(self, *args, **kwargs):
        args = list(args)
        if args and callable(args[0]):
            func = self._func = args[0]
            def key_func(key):
                "Apply key function to ``mapping[value]``."
                return func(self[key])
            args[0] = key_func
        else:
            self._func = None
            def key_func(key):
                "Return mapping value for key."
                return self[key]
            if args and args[0] is None:
                args[0] = key_func
            else:
                args.insert(0, key_func)
        super(ValueSortedDict, self).__init__(*args, **kwargs)

    def __delitem__(self, key):
        "``del mapping[key]``"
        if key not in self:
            raise KeyError(key)
        self._list_remove(key)
        dict.__delitem__(self, key)

    def __setitem__(self, key, value):
        "``mapping[key] = value``"
        if key in self:
            self._list_remove(key)
            dict.__delitem__(self, key)
        dict.__setitem__(self, key, value)
        self._list_add(key)

    _setitem = __setitem__

    def copy(self):
        "Return shallow copy of the mapping."
        return self.__class__(self._func, iter(self.items()))

    __copy__ = copy

    def __reduce__(self):
        items = [(key, self[key]) for key in self._list]
        args = (self._func, items)
        return (self.__class__, args)

    @recursive_repr()
    def __repr__(self):
        temp = '{0}({1}, {{{2}}})'
        items = ', '.join('{0}: {1}'.format(repr(key), repr(self[key]))
                          for key in self._list)
        return temp.format(
            self.__class__.__name__,
            repr(self._func),
            items
        )


class OrderedSet(abc.MutableSet, abc.Sequence):
    """Like OrderedDict, OrderedSet maintains the insertion order of elements.

    For example::

        >>> ordered_set = OrderedSet('abcde')
        >>> list(ordered_set) == list('abcde')
        True
        >>> ordered_set = OrderedSet('edcba')
        >>> list(ordered_set) == list('edcba')
        True

    OrderedSet also implements the collections.Sequence interface.

    """
    # pylint: disable=too-many-ancestors
    def __init__(self, iterable=()):
        # pylint: disable=super-init-not-called
        self._keys = {}
        self._nums = SortedDict()
        self._keys_view = self._nums.keys()
        self._count = count()
        self |= iterable

    def __contains__(self, key):
        "``key in ordered_set``"
        return key in self._keys

    count = __contains__

    def __iter__(self):
        "``iter(ordered_set)``"
        return iter(self._nums.values())

    def __reversed__(self):
        "``reversed(ordered_set)``"
        _nums = self._nums
        for key in reversed(_nums):
            yield _nums[key]

    def __getitem__(self, index):
        "``ordered_set[index]`` -> element; lookup element at index."
        num = self._keys_view[index]
        return self._nums[num]

    def __len__(self):
        "``len(ordered_set)``"
        return len(self._keys)

    def index(self, value):
        "Return index of value."
        # pylint: disable=arguments-differ
        try:
            return self._keys[value]
        except KeyError:
            raise ValueError('%r is not in %s' % (value, type(self).__name__))

    def add(self, value):
        "Add element, value, to set."
        if value not in self._keys:
            num = next(self._count)
            self._keys[value] = num
            self._nums[num] = value

    def discard(self, value):
        "Remove element, value, from set if it is a member."
        num = self._keys.pop(value, None)
        if num is not None:
            del self._nums[num]

    def __repr__(self):
        "Text representation of set."
        return '%s(%r)' % (type(self).__name__, list(self))

    __str__ = __repr__


class SegmentList(SortedKeyList):
    """List that supports fast random insertion and deletion of elements.

    SegmentList is a special case of a SortedList initialized with a key
    function that always returns 0. As such, several SortedList methods are not
    implemented for SegmentList.

    """
    # pylint: disable=too-many-ancestors
    def __init__(self, iterable=()):
        super(SegmentList, self).__init__(iterable, self.zero)

    @staticmethod
    def zero(_):
        "Return 0."
        return 0

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            raise NotImplementedError
        pos, idx = self._pos(index)
        self._lists[pos][idx] = value

    def append(self, value):
        if self._len:
            pos = len(self._lists) - 1
            self._lists[pos].append(value)
            self._keys[pos].append(0)
            self._expand(pos)
        else:
            self._lists.append([value])
            self._keys.append([0])
            self._maxes.append(0)
        self._len += 1

    def extend(self, values):
        for value in values:
            self.append(value)

    def insert(self, index, value):
        if index == self._len:
            self.append(value)
            return
        pos, idx = self._pos(index)
        self._lists[pos].insert(idx, value)
        self._keys[pos].insert(idx, 0)
        self._expand(pos)
        self._len += 1

    def reverse(self):
        values = list(self)
        values.reverse()
        self.clear()
        self.extend(values)

    def sort(self, key=None, reverse=False):
        "Stable sort in place."
        values = sorted(self, key=key, reverse=reverse)
        self.clear()
        self.extend(values)

    def _not_implemented(self, *args, **kwargs):
        "Not implemented."
        raise NotImplementedError

    add = _not_implemented
    bisect = _not_implemented
    bisect_left = _not_implemented
    bisect_right = _not_implemented
    bisect_key = _not_implemented
    bisect_key_left = _not_implemented
    bisect_key_right = _not_implemented
    irange = _not_implemented
    irange_key = _not_implemented
    update = _not_implemented
