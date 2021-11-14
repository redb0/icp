"""Tests for Rectangle class from base.py

:Date: 06.11.2021
:Authors:
    - Voronov Vladimir
"""

import pytest

from ..base import Rectangle


@pytest.mark.parametrize(
    'length, width, coord',
    [
        (1, 1, None),
        (5, 10, (0, 0)),
        (8, 2, (1, 1)),
    ]
)
def test_create(length, width, coord):
    """Instantiation tests for Rectangle class"""
    rect = Rectangle(length, width, coord)
    assert rect.length == length
    assert rect.width == width
    assert rect.size == (length, width)
    if coord is None:
        assert rect.coord == (0, 0)
    else:
        assert rect.coord == coord


@pytest.mark.parametrize(
    'length, width, coord',
    [
        (1, 1, None),
        (5, 10, (0, 0)),
        (8, 2, (1, 1)),
        (0, 0, (2, 0)),
        (2, 1, (0, 3)),
    ]
)
def test_corners(length, width, coord):
    """Test for calculating corners of a rectangle"""
    rect = Rectangle(length, width, coord)

    if coord is None:
        coord = (0, 0)

    assert rect.blp == coord
    assert (rect.x, rect.y) == coord
    assert rect.brp == (coord[0] + width, coord[1])
    assert rect.tlp == (coord[0], coord[1] + length)
    assert rect.trp == (coord[0] + width, coord[1] + length)


@pytest.mark.parametrize(
    'length, width, coord',
    [
        (1, 1, None),
        (5, 10, (0, 0)),
        (8, 2, (1, 1)),
        (0, 0, (2, 0)),
        (2, 1, (0, 3)),
    ]
)
def test_area(length, width, coord):
    """Area property test"""
    rect = Rectangle(length, width, coord)
    assert rect.area == length * width


@pytest.mark.parametrize(
    'length, width, coord',
    [
        (1, 1, None),
        (5, 10, (0, 0)),
        (8, 2, (1, 1)),
        (0, 0, (2, 0)),
        (2, 1, (0, 3)),
    ]
)
def test_diagonal(length, width, coord):
    """Diagonal property test"""
    rect = Rectangle(length, width, coord)
    assert rect.diagonal == (length**2 + width**2) ** 0.5


@pytest.mark.parametrize(
    'rect_a, rect_b, expected',
    [
        ((1, 1, None), (1, 1, None), True),
        ((5, 10, (0, 0)), (5, 10, (0, 0)), True),
        ((8, 2, (1, 1)), (8, 2, (1, 1)), True),
        ((5, 5, (2, 0)), (5, 5, (2, 0)), True),
        ((2, 1, (0, 3)), 'qwe', False),
        ((2, 1, (0, 3)), (1, 1, (0, 3)), False),
        ((2, 1, (0, 3)), (2, 0, (0, 3)), False),
        ((2, 1, (0, 3)), (2, 1, (1, 3)), False),
        ((2, 1, (0, 3)), (2, 1, (0, 2)), False),
    ]
)
def test_eq(rect_a, rect_b, expected):
    """Rectangle comparison test"""
    rect_a = Rectangle(*rect_a)
    rect_b = Rectangle(*rect_b)
    assert (rect_a == rect_b) is expected


@pytest.mark.parametrize(
    'length, width, coord',
    [
        (1, 1, None),
        (5, 10, (0, 0)),
        (8, 2, (1, 1)),
        (5, 5, (2, 0)),
    ]
)
def test_rotate(length, width, coord):
    """Rectangle rotation test"""
    rect = Rectangle(length, width, coord)
    rect.rotate()
    assert rect.size == (width, length)
    if coord is None:
        coord = (0, 0)
    assert rect.coord == coord


@pytest.mark.parametrize(
    'rect_a, rect_b, expected',
    [
        # без пересечения
        ((5, 10, (0, 0)), (5, 10, (20, 20)), None),
        ((8, 2, (1, 1)), (10, 1, (0, 0)), None),
        ((8, 2, (1, 1)), (1, 10, (0, 0)), None),
        # полностью накладываются
        ((5, 5, None), (5, 5, None), Rectangle(5, 5)),
        ((5, 5, (1, 1)), (10, 10, None), Rectangle(5, 5, (1, 1))),
        # внутри
        ((5, 5, None), (2, 2, None), Rectangle(2, 2)),
        ((5, 5, None), (2, 2, (1, 1)), Rectangle(2, 2, (1, 1))),
        # полностью одной стороной
        ((5, 5, (2, 2)), (10, 10, (5, 0)), Rectangle(5, 2, (5, 2))),
        ((5, 5, (2, 2)), (10, 10, (0, 5)), Rectangle(2, 5, (2, 5))),
        ((5, 5, (2, 2)), (5, 5, (2, 5)), Rectangle(2, 5, (2, 5))),
        ((5, 5, (2, 2)), (5, 5, (2, 5)), Rectangle(2, 5, (2, 5))),
        # углом
        ((5, 5, (5, 5)), (4, 4, (2, 2)), Rectangle(1, 1, (5, 5))),
        ((5, 5, (5, 5)), (4, 4, (8, 2)), Rectangle(1, 2, (8, 5))),
        ((5, 5, (5, 5)), (4, 4, (2, 8)), Rectangle(2, 1, (5, 8))),
        ((5, 5, (5, 5)), (4, 4, (8, 8)), Rectangle(2, 2, (8, 8))),
        # частично одной стороной
        ((5, 5, (5, 5)), (2, 4, (8, 7)), Rectangle(2, 2, (8, 7))),
        ((5, 5, (5, 5)), (2, 4, (3, 7)), Rectangle(2, 2, (5, 7))),
        ((5, 5, (5, 5)), (4, 2, (7, 8)), Rectangle(2, 2, (7, 8))),
        ((5, 5, (5, 5)), (4, 2, (7, 3)), Rectangle(2, 2, (7, 5))),
    ]
)
def test_intersection_without(rect_a, rect_b, expected):
    """Intersection rectangle test"""
    rect_a = Rectangle(*rect_a)
    rect_b = Rectangle(*rect_b)
    result = rect_a.intersection(rect_b)
    assert result == expected


@pytest.mark.parametrize(
    'rect_a, rect_b, expected',
    [
        # не совпадают
        ((5, 10, (0, 0)), (5, 10, (20, 20)), [Rectangle(5, 10)]),
        ((8, 2, (1, 1)), (10, 1, (0, 0)), [Rectangle(8, 2, (1, 1))]),
        ((8, 2, (1, 1)), (1, 10, (0, 0)), [Rectangle(8, 2, (1, 1))]),
        # совпадают
        ((5, 5, None), (5, 5, None), []),
        ((5, 5, (1, 1)), (10, 10, None), []),
        # внутри
        ((5, 5, None), (2, 2, (1, 1)), [
            Rectangle(1, 1, (0, 0)), Rectangle(2, 1, (0, 1)),
            Rectangle(2, 1, (0, 3)), Rectangle(1, 2, (1, 0)),
            Rectangle(2, 2, (1, 3)), Rectangle(1, 2, (3, 0)),
            Rectangle(2, 2, (3, 1)), Rectangle(2, 2, (3, 3))
        ]),
        # полностью одной стороной
        ((5, 5, (2, 2)), (10, 10, (5, 0)), [Rectangle(5, 3, (2, 2))]),
        ((5, 5, (2, 2)), (10, 10, (0, 5)), [Rectangle(3, 5, (2, 2))]),
        ((5, 5, (2, 2)), (5, 5, (2, 5)), [Rectangle(3, 5, (2, 2))]),
        ((5, 5, (2, 2)), (5, 5, (2, 5)), [Rectangle(3, 5, (2, 2))]),
        # углом
        ((5, 5, (5, 5)), (4, 4, (2, 2)), [
            Rectangle(4, 1, (5, 6)), Rectangle(1, 4, (6, 5)),
            Rectangle(4, 4, (6, 6))
        ]),
        ((5, 5, (5, 5)), (4, 4, (8, 2)), [
            Rectangle(1, 3, (5, 5)), Rectangle(4, 3, (5, 6)),
            Rectangle(4, 2, (8, 6))
        ]),
        ((5, 5, (5, 5)), (4, 4, (2, 8)), [
            Rectangle(3, 1, (5, 5)), Rectangle(3, 4, (6, 5)),
            Rectangle(2, 4, (6, 8))
        ]),
        ((5, 5, (5, 5)), (4, 4, (8, 8)), [
            Rectangle(3, 3, (5, 5)), Rectangle(2, 3, (5, 8)),
            Rectangle(3, 2, (8, 5))
        ]),
        # частично одной стороной
        ((5, 5, (5, 5)), (2, 4, (8, 7)), [
            Rectangle(2, 3, (5, 5)), Rectangle(2, 3, (5, 7)),
            Rectangle(1, 3, (5, 9)), Rectangle(2, 2, (8, 5)),
            Rectangle(1, 2, (8, 9)),
        ]),
        ((5, 5, (5, 5)), (2, 4, (3, 7)), [
            Rectangle(2, 2, (5, 5)), Rectangle(1, 2, (5, 9)),
            Rectangle(2, 3, (7, 5)), Rectangle(2, 3, (7, 7)),
            Rectangle(1, 3, (7, 9)),
        ]),
        ((5, 5, (5, 5)), (4, 2, (7, 8)), [
            Rectangle(3, 2, (5, 5)), Rectangle(2, 2, (5, 8)),
            Rectangle(3, 2, (7, 5)), Rectangle(3, 1, (9, 5)),
            Rectangle(2, 1, (9, 8)),
        ]),
        ((5, 5, (5, 5)), (4, 2, (7, 3)), [
            Rectangle(2, 2, (5, 5)), Rectangle(3, 2, (5, 7)),
            Rectangle(3, 2, (7, 7)), Rectangle(2, 1, (9, 5)),
            Rectangle(3, 1, (9, 7)),
        ]),
    ]
)
def test_difference(rect_a, rect_b, expected):
    """Difference rectangle test"""
    rect_a = Rectangle(*rect_a)
    rect_b = Rectangle(*rect_b)
    result = rect_a.difference(rect_b)
    assert list(result) == expected
