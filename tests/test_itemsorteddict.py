"Test sortedcollections.ItemSortedDict"

import copy

import pytest

from sortedcollections import ItemSortedDict


def key_func(key, value):
    return key


def value_func(key, value):
    return value


alphabet = 'abcdefghijklmnopqrstuvwxyz'


def test_init():
    temp = ItemSortedDict(key_func)
    temp._check()


def test_init_args():
    temp = ItemSortedDict(key_func, enumerate(alphabet))
    assert len(temp) == 26
    assert temp[0] == 'a'
    assert temp[25] == 'z'
    assert temp.keys()[4] == 4
    temp._check()


def test_init_kwargs():
    temp = ItemSortedDict(key_func, a=0, b=1, c=2)
    assert len(temp) == 3
    assert temp['a'] == 0
    assert temp.keys()[0] == 'a'
    temp._check()


def test_getitem():
    temp = ItemSortedDict(value_func, enumerate(reversed(alphabet)))
    assert temp[0] == 'z'
    assert temp.keys()[0] == 25
    assert list(temp) == list(reversed(range(26)))


def test_delitem():
    temp = ItemSortedDict(value_func, enumerate(reversed(alphabet)))
    del temp[25]
    assert temp.keys()[0] == 24


def test_delitem_error():
    temp = ItemSortedDict(value_func, enumerate(reversed(alphabet)))
    with pytest.raises(KeyError):
        del temp[-1]


def test_setitem():
    temp = ItemSortedDict(value_func, enumerate(reversed(alphabet)))
    temp[25] = '!'
    del temp[25]
    iloc = temp.keys()
    assert iloc[0] == 24
    temp[25] = 'a'
    assert iloc[0] == 25


def test_copy():
    temp = ItemSortedDict(value_func, enumerate(reversed(alphabet)))
    that = temp.copy()
    assert temp == that
    assert temp._key != that._key


def test_deepcopy():
    temp = ItemSortedDict(value_func, enumerate(reversed(alphabet)))
    that = copy.deepcopy(temp)
    assert temp == that
    assert temp._key != that._key


def test_update():
    temp = ItemSortedDict(lambda key, value: value)
    for index, letter in enumerate(alphabet):
        pair = {index: letter}
        temp.update(pair)
