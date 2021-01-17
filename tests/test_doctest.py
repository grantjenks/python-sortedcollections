import doctest

import sortedcollections
import sortedcollections.ordereddict
import sortedcollections.recipes


def test_sortedcollections():
    failed, attempted = doctest.testmod(sortedcollections)
    assert attempted > 0
    assert failed == 0


def test_sortedcollections_ordereddict():
    failed, attempted = doctest.testmod(sortedcollections.ordereddict)
    assert attempted > 0
    assert failed == 0


def test_sortedcollections_recipes():
    failed, attempted = doctest.testmod(sortedcollections.recipes)
    assert attempted > 0
    assert failed == 0
