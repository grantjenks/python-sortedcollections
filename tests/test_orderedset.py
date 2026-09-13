"Test sortedcollections.OrderedSet."

import random

import pytest

from sortedcollections import OrderedSet


def test_init():
    os = OrderedSet()
    assert len(os) == 0


def test_contains():
    os = OrderedSet(range(100))
    assert len(os) == 100
    for value in range(100):
        assert value in os
        assert os.count(value) == 1
    assert -1 not in os
    assert 100 not in os


def test_iter():
    os = OrderedSet(range(100))
    assert list(os) == list(range(100))
    names = ['eve', 'carol', 'alice', 'dave', 'bob']
    os = OrderedSet(names)
    assert list(os) == names


def test_reversed():
    os = OrderedSet(range(100))
    assert list(reversed(os)) == list(reversed(range(100)))
    names = ['eve', 'carol', 'alice', 'dave', 'bob']
    os = OrderedSet(names)
    assert list(reversed(os)) == list(reversed(names))


def test_getitem():
    values = list(range(100))
    random.shuffle(values)
    os = OrderedSet(values)
    assert len(os) == len(values)
    for index in range(len(os)):
        assert os[index] == values[index]


def test_index():
    values = list(range(100))
    random.shuffle(values)
    os = OrderedSet(values)
    assert len(os) == len(values)
    for value in values:
        assert values.index(value) == os.index(value)


@pytest.mark.parametrize('removed', ['a', 'c', 'ace'])
def test_index_after_discard(removed):
    os = OrderedSet('abcde')
    for value in removed:
        os.discard(value)
    expected = [value for value in 'abcde' if value not in removed]
    for index, value in enumerate(expected):
        assert os.index(value) == index
        assert os[os.index(value)] == value
    for value in removed:
        with pytest.raises(ValueError):
            os.index(value)


def test_index_after_clear():
    os = OrderedSet('abc')
    os.clear()
    os.add('d')
    assert os.index('d') == 0
    assert os[os.index('d')] == 'd'


def test_index_after_reinsert():
    os = OrderedSet('abc')
    os.discard('b')
    os.add('b')
    for index, value in enumerate('acb'):
        assert os.index(value) == index
        assert os[os.index(value)] == value


def test_index_error():
    os = OrderedSet(range(10))
    with pytest.raises(ValueError):
        os.index(10)


def test_add():
    os = OrderedSet()
    for value in range(100):
        os.add(value)
    assert len(os) == 100
    os.add(0)
    assert len(os) == 100
    for value in range(100):
        assert value in os


def test_discard():
    os = OrderedSet(range(100))
    for value in range(200):
        os.discard(value)
    assert len(os) == 0


def test_repr():
    os = OrderedSet()
    assert repr(os) == 'OrderedSet([])'
