"Test sortedcollections.recipes"

from nose.tools import raises
from sortedcollections import IndexableDict, IndexableSet, SegmentList


def test_index_dict():
    mapping = IndexableDict(enumerate(range(10)))
    for value in range(10):
        assert mapping.iloc[value] == value

def test_index_set():
    set_values = IndexableSet(range(10))
    for index in range(10):
        assert set_values[index] == index

def test_segment_list():
    values = [5, 1, 3, 2, 4, 8, 6, 7, 9, 0]
    sl = SegmentList(values)
    assert list(sl) == values
    sl.sort()
    assert list(sl) == list(range(10))

@raises(NotImplementedError)
def test_segment_list_error():
    sl = SegmentList()
    sl.bisect(0)
