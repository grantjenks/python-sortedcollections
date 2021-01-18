"""NearestDict implementation.

One primary use case for this data structure is storing data by a
`datetime.datetime` or `float` key.
"""

from sortedcontainers import SortedDict


class NearestDict(SortedDict):
    """A dict using nearest-key lookup.

    A :class:`SortedDict` subclass that uses nearest-key lookup instead of
    exact-key lookup. Optionally, you can specify a rounding mode to return the
    nearest key less than or equal to or greater than or equal to the provided
    key.

    When using :attr:`NearestDict.NEAREST` the keys must support subtraction to
    allow finding the nearest key (by find the key with the smallest difference
    to the given one).

    Additional methods:

    * :meth:`NearestDict.nearest_key`

    Example usage:

    >>> d = NearestDict({1.0: 'foo'})
    >>> d[1.0]
    'foo'
    >>> d[0.0]
    'foo'
    >>> d[2.0]
    'foo'
    """

    NEAREST_PREV = -1
    NEAREST = 0
    NEAREST_NEXT = 1

    def __init__(self, *args, **kwargs):
        """Initialize a NearestDict instance.

        Optional `rounding` argument dictates how
        :meth:`NearestDict.nearest_key` rounds. It must be one of
        :attr:`NearestDict.NEAREST_NEXT`, :attr:`NearestDict.NEAREST`, or
        :attr:`NearestDict.NEAREST_PREV`. (Default:
        :attr:`NearestDict.NEAREST`)

        :params rounding: how to round on nearest-key lookup (optional)
        :params args: positional arguments for :class:`SortedDict`.
        :params kwargs: keyword arguments for :class:`SortedDict`.
        """
        self.rounding = kwargs.pop('rounding', self.NEAREST)
        super().__init__(*args, **kwargs)

    def nearest_key(self, request):
        """Return nearest-key to `request`, respecting `self.rounding`.

        >>> d = NearestDict({1.0: 'foo'})
        >>> d.nearest_key(0.0)
        1.0
        >>> d.nearest_key(2.0)
        1.0

        >>> d = NearestDict({1.0: 'foo'}, rounding=NearestDict.NEAREST_PREV)
        >>> d.nearest_key(0.0)
        Traceback (most recent call last):
          ...
        KeyError: 'No key below 0.0 found'
        >>> d.nearest_key(2.0)
        1.0

        :param request: nearest-key lookup value
        :return: key nearest to `request`, respecting `rounding`
        :raises KeyError: if no appropriate key can be found
        """
        key_list = self.keys()

        if not key_list:
            raise KeyError('NearestDict is empty')

        index = self.bisect_left(request)

        if index >= len(key_list):
            if self.rounding == self.NEAREST_NEXT:
                raise KeyError('No key above {} found'.format(repr(request)))
            return key_list[index - 1]
        if key_list[index] == request:
            return key_list[index]
        if index == 0 and self.rounding == self.NEAREST_PREV:
            raise KeyError('No key below {} found'.format(repr(request)))
        if self.rounding == self.NEAREST_PREV:
            return key_list[index - 1]
        if self.rounding == self.NEAREST_NEXT:
            return key_list[index]
        if abs(key_list[index - 1] - request) < abs(key_list[index] - request):
            return key_list[index - 1]
        return key_list[index]

    def __getitem__(self, request):
        """Return item corresponding to :meth:`.nearest_key`.

        :param request: nearest-key lookup value
        :return: item corresponding to key nearest `request`
        :raises KeyError: if no appropriate item can be found

        >>> d = NearestDict({1.0: 'foo'})
        >>> d[0.0]
        'foo'
        >>> d[2.0]
        'foo'

        >>> d = NearestDict({1.0: 'foo'}, rounding=NearestDict.NEAREST_NEXT)
        >>> d[0.0]
        'foo'
        >>> d[2.0]
        Traceback (most recent call last):
          ...
        KeyError: 'No key above 2.0 found'
        """
        key = self.nearest_key(request)
        return super().__getitem__(key)
