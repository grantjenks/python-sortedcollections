import collections as co
from itertools import count
from sortedcontainers import SortedListWithKey, SortedDict, SortedSet


class IndexableDict(SortedDict):
    "Dictionary that supports numerical indexing."
    def __init__(self, *args, **kwargs):
        super(IndexableDict, self).__init__(hash, *args, **kwargs)


class IndexableSet(SortedSet):
    "Set that supports numerical indexing."
    def __init__(self, *args, **kwargs):
        super(IndexableSet, self).__init__(*args, key=hash, **kwargs)


class ItemSortedDict(SortedDict):
    "SortedDict requiring key function with `(key, value)` parameters."
    def __init__(self, *args, **kwargs):
        assert len(args) > 0 and callable(args[0])
        args = list(args)
        func = self._func = args[0]
        def key_func(key):
            return func(key, self[key])
        args[0] = key_func
        super(ItemSortedDict, self).__init__(*args, **kwargs)

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(key)
        self._list_remove(key)
        self._delitem(key)

    def __setitem__(self, key, value):
        if key in self:
            self._list_remove(key)
            self._delitem(key)
        self._setitem(key, value)
        self._list_add(key)

    def copy(self):
        "Return shallow copy of the sorted dictionary."
        return self.__class__(self._func, self._load, self.iteritems())

    __copy__ = copy


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
                return func(self[key])
            args[0] = key_func
        else:
            self._func = None
            def key_func(key):
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
        self._delitem(key)

    def __setitem__(self, key, value):
        "``mapping[key] = value``"
        if key in self:
            self._list_remove(key)
            self._delitem(key)
        self._setitem(key, value)
        self._list_add(key)

    def copy(self):
        "Return shallow copy of the mapping."
        return self.__class__(self._func, self._load, self.iteritems())

    __copy__ = copy


class OrderedSet(co.MutableSet, co.Sequence):
    def __init__(self, iterable=()):
        self._keys = {}
        self._nums = SortedDict()
        self._count = count()
        self |= iterable

    def __contains__(self, key):
        return key in self._keys

    count = __contains__

    def __iter__(self):
        return self._nums.itervalues()

    def __reversed__(self):
        _nums = self._nums
        for key in reversed(_nums):
            yield _nums[key]

    def __getitem__(self, index):
        _nums = self._nums
        num = _nums._list[index]
        return _nums[num]

    def __len__(self):
        return len(self._keys)

    def index(self, key):
        try:
            return self._keys[key]
        except KeyError:
            raise ValueError('%r is not in %s' % (key, type(self).__name__))

    def add(self, key):
        if key not in self._keys:
            num = next(self._count)
            self._keys[key] = num
            self._nums[num] = key

    def discard(self, key):
        num = self._keys.pop(key, None)
        if num is not None:
            del self._nums[num]

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, list(self))

    __str__ = __repr__


class SegmentList(SortedListWithKey):
    def __init__(self, iterable=()):
        super(SegmentList, self).__init__(iterable, self.zero)

    @staticmethod
    def zero(value):
        return 0

    def sort(self, key=None, reverse=False):
        self[:] = sorted(self, key=key, reverse=reverse)

    def _not_implemented(self, *args, **kwargs):
        raise NotImplementedError

    bisect = _not_implemented
    bisect_left = _not_implemented
    bisect_right = _not_implemented
    bisect_key = _not_implemented
    bisect_key_left = _not_implemented
    bisect_key_right = _not_implemented
