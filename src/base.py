"""Base class module

Module contains:
    - Rectangle - base class of rectangle

:Date: 06.11.2021
:Authors:
    - Voronov Vladimir
"""

from operator import attrgetter
from typing import Iterable

from .types import Number, Coord, Size


class Rectangle:
    """Rectangle class on a 2D plane

    :param _length: Length of rectangle
    :type _length: int | float
    :param _width: Width of rectangle
    :type _width: int | float
    :param _coord: Coordinates of lower-left corner of rectangle
    :type _coord: tuple[int | float, int | float]
    """
    def __init__(self, length: Number, width: Number,
                 coord: Coord | None=None) -> None:
        self._length = length
        self._width = width
        self._coord = coord if coord else (0, 0)

    def rotate(self) -> None:
        """Rotate rectangle 90 degrees"""
        self.width, self.length = self.length, self.width

    @property
    def length(self) -> Number:
        """Length of rectangle"""
        return self._length

    @length.setter
    def length(self, value: Number) -> None:
        self._length = value

    @property
    def width(self) -> Number:
        """Width of rectangle"""
        return self._width

    @width.setter
    def width(self, value: Number) -> None:
        self._width = value

    @property
    def coord(self) -> Coord:
        """Coordinates of lower-left corner of rectangle"""
        return self._coord

    @coord.setter
    def coord(self, value: Coord) -> None:
        self._coord = value

    @property
    def x(self) -> Number:
        """Coordinate X of lower-left corner of rectangle"""
        return self._coord[0]

    @property
    def y(self) -> Number:
        """Coordinate Y of lower-left corner of rectangle"""
        return self._coord[1]

    @property
    def trp(self) -> Coord:
        """Top right point

          #----------- trp
          |             |
          h             |
          |             |
        coord --- w ----#
        """
        return (self.coord[0] + self.width, self.coord[1] + self.length)

    @property
    def tlp(self) -> Coord:
        """Top left point

         tlp -----------#
          |             |
          h             |
          |             |
        coord --- w ----#
        """
        return (self.coord[0], self.coord[1] + self.length)

    @property
    def brp(self) -> Coord:
        """Bottom right point

          #-------------#
          |             |
          h             |
          |             |
        coord --- w -- brp
        """
        return (self.coord[0] + self.width, self.coord[1])

    @property
    def blp(self) -> Coord:
        """Bottom left point

         #-------------#
         |             |
         h             |
         |             |
        blp --- w -----#
        """
        return self.coord

    @property
    def area(self) -> Number:
        """Area of a rectangle"""
        return self.length * self.width

    @property
    def diagonal(self):
        """Diagonal of rectangle"""
        return (self.length**2 + self.width**2) ** 0.5

    @property
    def size(self) -> Size:
        """Size of rectangle (length, width)"""
        return self.length, self.width

    @size.setter
    def size(self, value: Size) -> None:
        """Size of rectangle (length, width)"""
        self.length, self.width = value


def min_enclosing_rect(rectangles: Iterable[Rectangle]) -> Rectangle:
    """Минимальный объемлющий прямоугольник

    Минимальный прямоугольник, который содержит заданный набор
    прямоугольников.

    :param rectangles: набор прямоугольников
    :type rectangles: Iterable[Rectangle]
    :return: минимальный объемлющий прямоугольник
    :rtype: Rectangle
    """
    blp_x = min(map(attrgetter('x'), rectangles))
    blp_y = min(map(attrgetter('y'), rectangles))
    trp_x = max(rect.trp[0] for rect in rectangles)
    trp_y = max(rect.trp[1] for rect in rectangles)
    return Rectangle(trp_y - blp_y, trp_x - blp_x, coord=(blp_x, blp_y))
