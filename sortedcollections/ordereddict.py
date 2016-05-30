import collections as co
from itertools import count
from operator import eq
from sortedcontainers import SortedDict
from sortedcontainers.sortedlist import recursive_repr
import sys

if sys.hexversion < 0x03000000:
    from itertools import imap
    map = imap

NONE = object()


class KeysView(co.KeysView):
    def __reversed__(self):
        return reversed(self._mapping)


class ItemsView(co.ItemsView):
    def __reversed__(self):
        for key in reversed(self._mapping):
            yield key, self._mapping[key]


class ValuesView(co.ValuesView):
    def __reversed__(self):
        for key in reversed(self._mapping):
            yield self._mapping[key]


class SequenceView(object):
    def __init__(self, nums):
        self._nums = nums

    def __len__(self):
        return len(self._nums)

    def __getitem__(self, index):
        num = self._nums.iloc[index]
        return self._nums[num]


class OrderedDict(dict):
    "Dictionary that remembers insertion order and is numerically indexable."
    def __init__(self, *args, **kwargs):
        self._keys = {}
        self._nums = nums = SortedDict()
        self._count = count()
        self.iloc = SequenceView(nums)
        self.update(*args, **kwargs)

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        if key not in self:
            num = next(self._count)
            self._keys[key] = num
            self._nums[num] = key
        dict_setitem(self, key, value)

    def __delitem__(self, key, dict_delitem=dict.__delitem__):
        dict_delitem(self, key)
        num = self._keys.pop(key)
        del self._nums[num]

    def __iter__(self):
        return self._nums.itervalues()

    def __reversed__(self):
        nums = self._nums
        for key in reversed(nums):
            yield nums[key]

    def clear(self, dict_clear=dict.clear):
        dict_clear(self)
        self._keys.clear()
        self._nums.clear()

    def popitem(self, last=True):
        index = -1 if last else 0
        num = self._nums.iloc[index]
        key = self._nums[num]
        value = self.pop(key)
        return key, value

    update = __update = co.MutableMapping.update

    def keys(self):
        return list(self.iterkeys())

    def items(self):
        return list(self.iteritems())

    def values(self):
        return list(self.itervalues())

    def iterkeys(self):
        return self._nums.itervalues()

    def iteritems(self):
        for key in self._nums.itervalues():
            yield key, self[key]

    def itervalues(self):
        for key in self._nums.itervalues():
            yield self[key]

    def viewkeys(self):
        return KeysView(self)

    def viewitems(self):
        return ItemsView(self)

    def viewvalues(self):
        return ValuesView(self)

    def pop(self, key, default=NONE):
        if key in self:
            value = self[key]
            del self[key]
            return value
        elif default is NONE:
            raise KeyError(key)
        else:
            return default

    def setdefault(self, key, default=None):
        'od.setdefault(k[,d]) -> od.get(k,d), also set od[k]=d if k not in od'
        if key in self:
            return self[key]
        self[key] = default
        return default

    @recursive_repr
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.items())

    __str__ = __repr__

    def __reduce__(self):
        return (self.__class__, (self.items(),))

    def copy(self):
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        return cls((key, value) for key in iterable)

    def __eq__(self, other):
        if isinstance(other, OrderedDict):
            return dict.__eq__(self, other) and all(map(eq, self, other))
        else:
            return dict.__eq__(self, other)

    __ne__ = co.MutableMapping.__ne__

    def _check(self):
        keys = self._keys
        nums = self._nums

        for key, value in keys.items():
            assert nums[value] == key

        nums._check()
