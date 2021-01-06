"Test sortedcollections.recipes"

import pickle, pytest
from sortedcollections import IndexableDict, IndexableSet, SegmentList


def test_index_dict():
    mapping = IndexableDict(enumerate(range(10)))
    iloc = mapping.keys()
    for value in range(10):
        assert iloc[value] == value

def test_index_set():
    set_values = IndexableSet(range(10))
    for index in range(10):
        assert set_values[index] == index

def test_index_set_pickle():
    set_values1 = IndexableSet(range(10))
    data = pickle.dumps(set_values1)
    set_values2 = pickle.loads(data)
    assert set_values1 == set_values2

def test_segment_list():
    values = [5, 1, 3, 2, 4, 8, 6, 7, 9, 0]
    sl = SegmentList(values)
    assert list(sl) == values
    sl.sort()
    assert list(sl) == list(range(10))
    sl.reverse()
    assert list(sl) == list(reversed(range(10)))
    sl.reverse()
    sl.append(10)
    assert list(sl) == list(range(11))
    sl.extend(range(11, 15))
    assert list(sl) == list(range(15))
    del sl[5:]
    assert list(sl) == list(range(5))
    sl[2] = 'c'
    sl.insert(3, 'd')
    sl.insert(6, 'e')
    assert list(sl) == [0, 1, 'c', 'd', 3, 4, 'e']

def test_segment_list_bisect():
    sl = SegmentList()
    with pytest.raises(NotImplementedError):
        sl.bisect(0)

def test_segment_list_setitem_slice():
    sl = SegmentList()
    with pytest.raises(NotImplementedError):
        sl[:] = [0]
