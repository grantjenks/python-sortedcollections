"Test sortedcollections.OrderedDict"

import pickle
import pytest
from sortedcollections import OrderedDict

pairs = dict(enumerate(range(10)))

def test_init():
    od = OrderedDict()
    assert len(od) == 0
    od._check()
    od = OrderedDict(enumerate(range(10)))
    assert len(od) == 10
    od._check()
    od = OrderedDict(a=0, b=1, c=2)
    assert len(od) == 3
    od._check()
    od = OrderedDict(pairs)
    assert len(od) == 10
    od._check()

def test_setitem():
    od = OrderedDict()
    od['alice'] = 0
    od['bob'] = 1
    od['carol'] = 2
    assert len(od) == 3
    od._check()

def test_delitem():
    od = OrderedDict(pairs)
    assert len(od) == 10
    for value in range(10):
        del od[value]
    assert len(od) == 0
    od._check()

def test_iter_reversed():
    od = OrderedDict([('b', 0), ('a', 1), ('c', 2)])
    assert list(od) == ['b', 'a', 'c']
    assert list(reversed(od)) == ['c', 'a', 'b']
    od._check()

def test_clear():
    od = OrderedDict(pairs)
    assert len(od) == 10
    od.clear()
    assert len(od) == 0
    od._check()

def test_popitem():
    od = OrderedDict(enumerate(range(10)))
    for num in reversed(range(10)):
        key, value = od.popitem()
        assert num == key == value
        od._check()

    od = OrderedDict(enumerate(range(10)))
    for num in range(10):
        key, value = od.popitem(last=False)
        assert num == key == value
        od._check()

def test_keys():
    od = OrderedDict(enumerate(range(10)))
    assert list(reversed(od.keys())) == list(reversed(range(10)))
    assert od.keys()[:3] == [0, 1, 2]
    od._check()

def test_items():
    items = list(enumerate(range(10)))
    od = OrderedDict(enumerate(range(10)))
    assert list(reversed(od.items())) == list(reversed(items))
    assert od.items()[:3] == [(0, 0), (1, 1), (2, 2)]
    od._check()

def test_values():
    od = OrderedDict(enumerate(range(10)))
    assert list(reversed(od.values())) == list(reversed(range(10)))
    assert od.values()[:3] == [0, 1, 2]
    od._check()

def test_iloc():
    od = OrderedDict(enumerate(range(10)))
    iloc = od.keys()
    for num in range(10):
        assert iloc[num] == num
    iloc[-1] == 9
    assert len(iloc) == 10
    od._check()

def test_pop():
    od = OrderedDict(enumerate(range(10)))
    for num in range(10):
        assert od.pop(num) == num
        od._check()
    assert od.pop(0, 'thing') == 'thing'
    assert od.pop(1, default='thing') == 'thing'
    od._check()

def test_pop_error():
    od = OrderedDict()
    with pytest.raises(KeyError):
        od.pop(0)

def test_setdefault():
    od = OrderedDict()
    od.setdefault(0, False)
    assert od[0] == False
    od.setdefault(1, default=True)
    assert od[1] == True
    od.setdefault(2)
    assert od[2] == None
    assert od.setdefault(0) == False
    assert od.setdefault(1) == True

def test_repr():
    od = OrderedDict()
    assert repr(od) == 'OrderedDict([])'
    assert str(od) == 'OrderedDict([])'

def test_reduce():
    od = OrderedDict(enumerate(range(10)))
    data = pickle.dumps(od)
    copy = pickle.loads(data)
    assert od == copy

def test_copy():
    od = OrderedDict(enumerate(range(10)))
    copy = od.copy()
    assert od == copy

def test_fromkeys():
    od = OrderedDict.fromkeys('abc')
    assert od == {'a': None, 'b': None, 'c': None}
    od._check()

def test_equality():
    od = OrderedDict.fromkeys('abc')
    assert od == {'a': None, 'b': None, 'c': None}
    assert od != {}
    assert od != OrderedDict()
    od._check()
