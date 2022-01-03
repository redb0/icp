"""Тесты для модуля estimate.py

:Date: 03.01.2022
:Authors:
    - Voronov Vladimir
"""

import pytest

from ..estimate import estimate_size


@pytest.mark.parametrize(
    'x, y, expected',
    [
        (0, 0, (12, 20)),
        (1, 1, (11, 19)),
        (5, 5, (7, 15)),
        (6, 10, (6, 10)),
        (0, 10, (12, 10)),
        (6, 0, (6, 20)),
    ]
)
def test_inner_rectangle(x, y, expected):
    """Тесты оценки для точки из внутреннего прямоугольника"""
    assert estimate_size(10, 6, 3, 1.5, x, y) == expected


@pytest.mark.parametrize(
    'x, y, expected',
    [
        (10, 5, (2, 7)),
        (5, 15, (3, 5)),
        (12, 8, (0, 2)),
        (5, 20, (1, 0)),
        (0, 20, (6, 0)),
        (12, 0, (0, 10)),
    ]
)
def test_side_rectangles(x, y, expected):
    """Тесты оценки для точки из верхнего левого и нижнего правого
    прямоугольников
    """
    assert estimate_size(10, 6, 3, 1.5, x, y) == expected


@pytest.mark.parametrize(
    'x, y, expected',
    [
        (8, 12, (2, 3)),
        (10, 12, (0, 0)),
    ]
)
def test_curved_part(x, y, expected):
    """Тесты оценки для точки из криволинейной части"""
    assert estimate_size(10, 6, 3, 1.5, x, y) == expected
