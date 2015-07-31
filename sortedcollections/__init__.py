# -*- coding: utf-8 -*-

"""
sortedcollections Sorted Collections
====================================

SortedCollections is an Apache2 licensed sorted collections library.

:copyright: (c) 2015 by Grant Jenks.
:license: Apache 2.0, see LICENSE for more details.

"""

__title__ = 'sortedcollections'
__version__ = '0.3.1'
__build__ = 0x000301
__author__ = 'Grant Jenks'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2015 Grant Jenks'

from sortedcontainers import (
    SortedList, SortedListWithKey, SortedDict, SortedSet
)

from .itemsorteddict import ItemSortedDict

__all__ = [
    'SortedList', 'SortedListWithKey', 'SortedSet', 'SortedDict'
    'ItemSortedDict',
]
