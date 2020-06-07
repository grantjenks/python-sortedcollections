import pytest

from sortedcollections import NearestDict


def test_basic():
    d = NearestDict()

    with pytest.raises(KeyError):
        d[0]

    d[0] = "a"
    assert d[0] == "a"
    d[0] = "b"
    assert d[0] == "b"


def test_iteration():
    # In sorted order by key
    exp_items = (
        (0, "a"),
        (1, "b"),
        (2, "c"),
    )

    d = NearestDict()
    for k, v in exp_items:
        d[k] = v

    for act, exp in zip(d.items(), exp_items):
        assert act == exp


def test_nearest():
    d = NearestDict(rounding=NearestDict.NEAREST)

    d[0] = "a"
    d[3] = "b"
    assert d[-1] == "a"
    assert d[0] == "a"
    assert d[1] == "a"
    assert d[2] == "b"
    assert d[3] == "b"
    assert d[4] == "b"


def test_nearest_prev():
    d = NearestDict(rounding=NearestDict.NEAREST_PREV)

    d[0] = "a"
    d[3] = "b"
    with pytest.raises(KeyError):
        d[-1]
    assert d[0] == "a"
    assert d[1] == "a"
    assert d[2] == "a"
    assert d[3] == "b"
    assert d[4] == "b"


def test_nearest_next():
    d = NearestDict(rounding=NearestDict.NEAREST_NEXT)

    d[0] = "a"
    d[3] = "b"
    assert d[-1] == "a"
    assert d[0] == "a"
    assert d[1] == "b"
    assert d[2] == "b"
    assert d[3] == "b"
    with pytest.raises(KeyError):
        d[4]
