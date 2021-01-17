"""Python Sorted Collections

SortedCollections is an Apache2 licensed Python sorted collections library.

:copyright: (c) 2015-2021 by Grant Jenks.
:license: Apache 2.0, see LICENSE for more details.

"""

from sortedcontainers import (
    SortedDict,
    SortedList,
    SortedListWithKey,
    SortedSet,
)

from .ordereddict import OrderedDict
from .recipes import (
    IndexableDict,
    IndexableSet,
    ItemSortedDict,
    OrderedSet,
    SegmentList,
    ValueSortedDict,
)

__all__ = [
    'IndexableDict',
    'IndexableSet',
    'ItemSortedDict',
    'OrderedDict',
    'OrderedSet',
    'SegmentList',
    'SortedDict',
    'SortedList',
    'SortedListWithKey',
    'SortedSet',
    'ValueSortedDict',
]

__version__ = '2.0.0'
