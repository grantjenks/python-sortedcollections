"Test sortedcollections.ValueSortedDict"

import pickle
from nose.tools import raises
from sortedcollections import ValueSortedDict

def identity(value):
    return value

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def test_init():
    temp = ValueSortedDict()
    temp._check()

def test_init_args():
    temp = ValueSortedDict(enumerate(alphabet))
    assert len(temp) == 26
    assert temp[0] == 'a'
    assert temp[25] == 'z'
    assert temp.keys()[4] == 4
    temp._check()

def test_init_kwargs():
    temp = ValueSortedDict(None, a=0, b=1, c=2)
    assert len(temp) == 3
    assert temp['a'] == 0
    assert temp.keys()[0] == 'a'
    temp._check()

def test_getitem():
    temp = ValueSortedDict(identity, enumerate(reversed(alphabet)))
    assert temp[0] == 'z'
    assert temp.keys()[0] == 25
    assert list(temp) == list(reversed(range(26)))

def test_delitem():
    temp = ValueSortedDict(identity, enumerate(reversed(alphabet)))
    del temp[25]
    assert temp.keys()[0] == 24

@raises(KeyError)
def test_delitem_error():
    temp = ValueSortedDict(identity, enumerate(reversed(alphabet)))
    del temp[-1]

def test_setitem():
    temp = ValueSortedDict(identity, enumerate(reversed(alphabet)))
    temp[25] = '!'
    del temp[25]
    assert temp.keys()[0] == 24
    temp[25] = 'a'
    assert temp.keys()[0] == 25

def test_copy():
    temp = ValueSortedDict(identity, enumerate(reversed(alphabet)))
    that = temp.copy()
    assert temp == that
    assert temp._key != that._key

def test_pickle():
    original = ValueSortedDict(identity, enumerate(reversed(alphabet)))
    data = pickle.dumps(original)
    duplicate = pickle.loads(data)
    assert original == duplicate

class Negater(object):
    def __call__(self, value):
        return -value
    def __repr__(self):
        return 'negate'

def test_repr():
    temp = ValueSortedDict(Negater())
    assert repr(temp) == 'ValueSortedDict(negate, {})'
