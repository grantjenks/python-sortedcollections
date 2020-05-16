import pytest

from sortedcollections import FuzzySortedDict


def test_basic():
    fsd = FuzzySortedDict()

    with pytest.raises(KeyError):
        fsd[0]

    fsd[0] = "a"
    assert fsd[0] == "a"
    fsd[0] = "b"
    assert fsd[0] == "b"


def test_iteration():
    # In sorted order by key
    exp_items = (
        (0, "a"),
        (1, "b"),
        (2, "c"),
    )

    fsd = FuzzySortedDict()
    for k, v in exp_items:
        fsd[k] = v

    for act, exp in zip(fsd.items(), exp_items):
        assert act == exp


def test_round_closest():
    fsd = FuzzySortedDict(rounding=FuzzySortedDict.ROUND_CLOSEST)

    fsd[0] = "a"
    fsd[3] = "b"
    assert fsd[-1] == "a"
    assert fsd[1] == "a"
    assert fsd[2] == "b"
    assert fsd[4] == "b"


def test_round_down():
    fsd = FuzzySortedDict(rounding=FuzzySortedDict.ROUND_DOWN)

    fsd[0] = "a"
    fsd[3] = "b"
    with pytest.raises(KeyError):
        fsd[-1]
    assert fsd[1] == "a"
    assert fsd[2] == "a"
    assert fsd[4] == "b"


def test_round_up():
    fsd = FuzzySortedDict(rounding=FuzzySortedDict.ROUND_UP)

    fsd[0] = "a"
    fsd[3] = "b"
    assert fsd[-1] == "a"
    assert fsd[1] == "b"
    assert fsd[2] == "b"
    with pytest.raises(KeyError):
        fsd[4]
