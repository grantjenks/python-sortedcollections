"""Python Sorted Collections

SortedCollections is an Apache2 licensed Python sorted collections library.

:copyright: (c) 2015-2018 by Grant Jenks.
:license: Apache 2.0, see LICENSE for more details.

"""

from sortedcontainers import (
    SortedList, SortedListWithKey, SortedDict, SortedSet
)

from .recipes import IndexableDict, IndexableSet
from .recipes import ItemSortedDict, ValueSortedDict
from .recipes import OrderedSet, SegmentList
from .ordereddict import OrderedDict

__title__ = 'sortedcollections'
__version__ = '1.2.3'
__build__ = 0x010203
__author__ = 'Grant Jenks'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2015-2018 Grant Jenks'
