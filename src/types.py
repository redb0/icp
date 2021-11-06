"""Type annotation helper module

:Date: 06.11.2021
:Authors:
    - Voronov Vladimir
"""

from typing import TypeAlias


Number: TypeAlias = int | float
Coord: TypeAlias = tuple[Number, Number]
# Size: TypeAlias = tuple[Number, Number] | list[Number]
Size: TypeAlias = tuple[Number, Number]
SizeList: TypeAlias = list[Size]
