from calc import add, subtract


def test_add() -> None:
    assert add(3, 8) == 11


def test_subtrac() -> None:
    assert subtract(5, 11) == 6
