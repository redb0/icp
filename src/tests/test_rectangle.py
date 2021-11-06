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
