from sortedcontainers import SortedDict

class KeyWrapper(object):
    "Wraps a key function and applies with `(key, value)` item."
    def __init__(self, func, _dict):
        self._func = func
        self._dict = _dict
    def __call__(self, key):
        "Apply key function to `(key, value)` item."
        return self._func(key, self._dict[key])

class ItemSortedDict(SortedDict):
    "Requires a key function that accepts two arguments: key, value."
    def __init__(self, *args, **kwargs):
        assert len(args) > 0 and callable(args[0])
        args = list(args)
        key = self._original_key = args[0]
        args[0] = KeyWrapper(key, self)
        super(ItemSortedDict, self).__init__(*args, **kwargs)

    def __delitem__(self, key):
        """
        Remove ``d[key]`` from *d*.
        Raise KeyError if *key* is not in the dictionary.
        """
        if key not in self:
            raise KeyError(key)
        self._list_remove(key)
        self._delitem(key)

    def __setitem__(self, key, value):
        """Set `d[key]` to *value*."""
        if key in self:
            self._list_remove(key)
            self._delitem(key)
        self._setitem(key, value)
        self._list_add(key)

    def copy(self):
        """Return a shallow copy of the sorted dictionary."""
        return self.__class__(self._original_key, self._load, self.iteritems())

    __copy__ = copy
