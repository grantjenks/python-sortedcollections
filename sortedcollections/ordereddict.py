"""Ordered dictionary implementation.

"""

import collections as co
from itertools import count
from operator import eq
import sys

from sortedcontainers import SortedDict
from sortedcontainers.sortedlist import recursive_repr

if sys.hexversion < 0x03000000:
    from itertools import imap # pylint: disable=no-name-in-module, ungrouped-imports, wrong-import-order
    map = imap # pylint: disable=redefined-builtin, invalid-name

NONE = object()


class KeysView(co.KeysView, co.Sequence):
    "Read-only view of mapping keys."
    # pylint: disable=too-few-public-methods,protected-access
    def __getitem__(self, index):
        "``keys_view[index]``"
        _nums = self._mapping._nums
        if isinstance(index, slice):
            nums = _nums._list[index]
            return [_nums[num] for num in nums]
        return _nums[_nums._list[index]]


class ItemsView(co.ItemsView, co.Sequence):
    "Read-only view of mapping items."
    # pylint: disable=too-few-public-methods,protected-access
    def __getitem__(self, index):
        "``items_view[index]``"
        _mapping = self._mapping
        _nums = _mapping._nums
        if isinstance(index, slice):
            nums = _nums._list[index]
            keys = [_nums[num] for num in nums]
            return [(key, _mapping[key]) for key in keys]
        num = _nums._list[index]
        key = _nums[num]
        return key, _mapping[key]


class ValuesView(co.ValuesView, co.Sequence):
    "Read-only view of mapping values."
    # pylint: disable=too-few-public-methods,protected-access
    def __getitem__(self, index):
        "``items_view[index]``"
        _mapping = self._mapping
        _nums = _mapping._nums
        if isinstance(index, slice):
            nums = _nums._list[index]
            keys = [_nums[num] for num in nums]
            return [_mapping[key] for key in keys]
        num = _nums._list[index]
        key = _nums[num]
        return _mapping[key]


class OrderedDict(dict):
    """Dictionary that remembers insertion order and is numerically indexable.

    Keys are numerically indexable using dict views. For example::

        >>> ordered_dict = OrderedDict.fromkeys('abcde')
        >>> keys = ordered_dict.keys()
        >>> keys[0]
        'a'
        >>> keys[-2:]
        ['d', 'e']

    The dict views support the sequence abstract base class.

    """
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        self._keys = {}
        self._nums = SortedDict()
        self._keys_view = self._nums.keys()
        self._count = count()
        self.update(*args, **kwargs)

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        "``ordered_dict[key] = value``"
        if key not in self:
            num = next(self._count)
            self._keys[key] = num
            self._nums[num] = key
        dict_setitem(self, key, value)

    def __delitem__(self, key, dict_delitem=dict.__delitem__):
        "``del ordered_dict[key]``"
        dict_delitem(self, key)
        num = self._keys.pop(key)
        del self._nums[num]

    def __iter__(self):
        "``iter(ordered_dict)``"
        return iter(self._nums.values())

    def __reversed__(self):
        "``reversed(ordered_dict)``"
        nums = self._nums
        for key in reversed(nums):
            yield nums[key]

    def clear(self, dict_clear=dict.clear):
        "Remove all items from mapping."
        dict_clear(self)
        self._keys.clear()
        self._nums.clear()

    def popitem(self, last=True):
        """Remove and return (key, value) item pair.

        Pairs are returned in LIFO order if last is True or FIFO order if
        False.

        """
        index = -1 if last else 0
        num = self._keys_view[index]
        key = self._nums[num]
        value = self.pop(key)
        return key, value

    update = __update = co.MutableMapping.update

    def keys(self):
        "Return set-like and sequence-like view of mapping keys."
        return KeysView(self)

    def items(self):
        "Return set-like and sequence-like view of mapping items."
        return ItemsView(self)

    def values(self):
        "Return set-like and sequence-like view of mapping values."
        return ValuesView(self)

    def pop(self, key, default=NONE):
        """Remove given key and return corresponding value.

        If key is not found, default is returned if given, otherwise raise
        KeyError.

        """
        if key in self:
            value = self[key]
            del self[key]
            return value
        if default is NONE:
            raise KeyError(key)
        return default

    def setdefault(self, key, default=None):
        """Return ``mapping.get(key, default)``, also set ``mapping[key] = default`` if
        key not in mapping.

        """
        if key in self:
            return self[key]
        self[key] = default
        return default

    @recursive_repr()
    def __repr__(self):
        "Text representation of mapping."
        return '%s(%r)' % (self.__class__.__name__, list(self.items()))

    __str__ = __repr__

    def __reduce__(self):
        "Support for pickling serialization."
        return (self.__class__, (list(self.items()),))

    def copy(self):
        "Return shallow copy of mapping."
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        """Return new mapping with keys from iterable.

        If not specified, value defaults to None.

        """
        return cls((key, value) for key in iterable)

    def __eq__(self, other):
        "Test self and other mapping for equality."
        if isinstance(other, OrderedDict):
            return dict.__eq__(self, other) and all(map(eq, self, other))
        return dict.__eq__(self, other)

    __ne__ = co.MutableMapping.__ne__

    def _check(self):
        "Check consistency of internal member variables."
        # pylint: disable=protected-access
        keys = self._keys
        nums = self._nums

        for key, value in keys.items():
            assert nums[value] == key

        nums._check()
