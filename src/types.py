"""Type annotation helper module

:Date: 06.11.2021
:Authors:
    - Voronov Vladimir
"""

from typing import Protocol, TypeAlias


Number: TypeAlias = int | float
Coord: TypeAlias = tuple[Number, Number]
# Size: TypeAlias = tuple[Number, Number] | list[Number]
Size: TypeAlias = tuple[Number, Number]
Point: TypeAlias = tuple[Number, Number]
SizeList: TypeAlias = list[Size]


class RectangleProtocol(Protocol):
    """Протокол прямоугольника"""
    length: Number
    width: Number
    is_rotatable: bool

    # @property
    # def size(self) -> Size:
    #     raise NotImplementedError

    def rotate(self) -> None:
        """Поворот на 90 градусов"""
        raise NotImplementedError

    @property
    def area(self) -> Number:
        """Площадь фигуры"""
        raise NotImplementedError
