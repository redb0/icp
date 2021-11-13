"""Base class module

Module contains:
    - Rectangle - base class of rectangle

:Date: 06.11.2021
:Authors:
    - Voronov Vladimir
"""

import itertools

from operator import attrgetter
from typing import Generator, Iterable, Optional, TypeVar

from .types import Number, Coord, Size


T = TypeVar('T')


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

    def intersection(self, other: 'Rectangle') -> Optional['Rectangle']:
        """Пересечение двух прямоугольников

        Основано на реализации пересечения из SFML_.
        .. _SFML: https://github.com/SFML/SFML/blob/12d81304e63e333174d943ba3ff572e38abd56e0/include/SFML/Graphics/Rect.inl#L109

        Также смотри `это обсуждение`_.
        .. _`это обсуждение`: https://stackoverflow.com/questions/25068538/intersection-and-difference-of-two-rectangles

        :param other: Второй прямоугольник с которым ищется пересечение.
        :type other: Rectangle
        :return: Прямоугольник как результат пересечения, или `None`,
                 если пересечения нет.
        :rtype: None | Rectangle
        """
        x = max(min(self.x, self.trp[0]), min(other.x, other.trp[0]))
        y = max(min(self.y, self.trp[1]), min(other.y, other.trp[1]))
        x_top_right_point = min(
            max(self.x, self.trp[0]), max(other.x, other.trp[0])
        )
        y_top_right_point = min(
            max(self.y, self.trp[1]), max(other.y, other.trp[1])
        )
        if x < x_top_right_point and y < y_top_right_point:
            length = y_top_right_point - y
            width = x_top_right_point - x
            return self.__class__(length, width, (x, y))
        return None

    def difference(self,
                   other: 'Rectangle') -> Generator['Rectangle', None, None]:
        """Разность двух прямоугольников

        Возвращает от 1 до 8 прямоугольников.
        Возможны следующие ситуации:
        - `other` находится вне текущего прямоугольника;
        - `other` полностью перекрывает текущий прямоугольник;
        - `other` находится внутри текущего прямоугольника;
        - `other` частично перекрывает текущий прямоугольник;

        Смотри `это обсуждение`_.
        .. _`это обсуждение`: https://stackoverflow.com/questions/25068538/intersection-and-difference-of-two-rectangles

        :param other: Вычитаемый прямоугольник.
        :type other: Rectangle
        :yield: Прямоугольники составляющие разность.
        :rtype: Generator['Rectangle', None, None]
        """
        inter = self & other
        if inter is None:
            yield self
            return

        xs = {self.x, self.trp[0]}
        ys = {self.y, self.trp[1]}

        if self.x < other.x < self.trp[0]:
            xs.add(other.x)
        if self.x < other.trp[0] < self.trp[0]:
            xs.add(other.trp[0])
        if self.y < other.y < self.trp[1]:
            ys.add(other.y)
        if self.y < other.trp[1] < self.trp[1]:
            ys.add(other.trp[1])

        for (x, x_trp), (y, y_trp) in itertools.product(pairwise(sorted(xs)),
                                                        pairwise(sorted(ys))):
            length, width = y_trp - y, x_trp - x
            rect = self.__class__(length, width, (x, y))
            if rect != inter:
                yield rect

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

    __and__ = intersection  # &
    __sub__ = difference  # -

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return (
            o.length == self.length and o.width == self.width and
            o.coord == self.coord
        )

    def __ne__(self, o: object) -> bool:
        return not o == self

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}'
            f'({self.length}, {self.width}, {self.coord})'
        )

    def __copy__(self) -> 'Rectangle':
        return Rectangle(self.length, self.width, self.coord)


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


def pairwise(iterable: Iterable[T]) -> Iterable[tuple[T, T]]:
    """Попарное объединение элементов

    >>> list(pairwise([1, 2, 3]))
    [(1, 2), (2, 3)]

    :param iterable: Итерируемый объект
    :type iterable: [type]
    :return: Последовательность пар
    :rtype: [type]
    """
    first, second = itertools.tee(iterable)
    next(second, None)
    return zip(first, second)
