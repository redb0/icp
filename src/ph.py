"""Модуль алгоритма приоритетной эвристики (PH)

Модуль предназначен для решения `задачи гильотинного раскроя`_. Она
заключается в размещении прямоугольных элементов в контейнере заданных
размеров с учетом сплошных резов от края до края.

.. _`задачи гильотинного раскроя`: https://en.wikipedia.org/wiki/Guillotine_cutting

Приоритетная эвристика `ph_bpp` основана на сопоставлении каждому
прямоугольнику приоритета на основе варианта его размещения. Соблюдение
гильотинных ограничений основано на рекурсивной упаковке подобластей.

Подробнее см.:
- https://www.sciencedirect.com/science/article/pii/S0020019015001519?via%3Dihub
"""

import math
import sys

from operator import attrgetter
from typing import Literal, TypeAlias

from .base import Rectangle
from .types import Number, Point, RectangleProtocol


SoftType: TypeAlias = Literal[1, 2, 3]
SortAttr: TypeAlias = Literal[
    'width', 'length', 'max', 'min', 'area', 'diagonal'
]
RectList: TypeAlias = list[RectangleProtocol]


def sort(rectangles: RectList,
         sorting: SortAttr='width') -> tuple[RectList, list[int]]:
    """Сортировка прямоугольников

    Сортируются индексы прямоугольников в исходном списке, а также
    создается новый список отсортированных прямоугольников. Сортировка
    совершается по невозрастанию выбранного параметра `sorting`.

    Возможны варианты сортировки:
    - по ширине `'width'`, по умолчанию
    - по длине `'length'`
    - по максимальной стороне `'max'`
    - по минимальной стороне `'min'`
    - по площади `'area'`
    - по диагонали `'diagonal'`

    :param rectangles: набор прямоугольников в виде списка
    :type rectangles: list[RectangleProtocol]
    :param sorting: параметр, задающий вариант сортировки, возможны
                    варианты: `'width'`, `'length'`, `'max'`, `'min'`,
                    `'area'`, `'diagonal'`, defaults to `'width'`
    :type sorting: str, optional
    :return: Отсортированный список прямоугольников и список индексов
             в отсортированном порядке исходного списка.
    :rtype: tuple[RectList, list[int]]
    :raises ValueError: В случае, если аргумент `sorting` имеет значение,
                        отличное от указанных, вызывается исключение.
    """
    if sorting not in ('width', 'length', 'max', 'min', 'area', 'diagonal'):
        raise ValueError('The algorithm only supports sorting by width '
                         f'or length but {sorting} was given.')

    key_func=None
    if sorting in ('width', 'length', 'area'):
        # key_func = attrgetter(sorting)
        key_func = lambda index: attrgetter(sorting)(rectangles[index])
    elif sorting == 'diagonal':
        key_func = lambda index: math.sqrt(
            rectangles[index].length ** 2 + rectangles[index].width ** 2
        )
    elif sorting == 'max':
        key_func = lambda index: max(
            rectangles[index].length, rectangles[index].width
        )
    else:
        key_func = lambda index: min(
            rectangles[index].length, rectangles[index].width
        )

    sorted_indices = sorted(
        range(len(rectangles)), key=key_func, reverse=True
    )
    sorted_rect = [rectangles[i] for i in sorted_indices]

    return sorted_rect, sorted_indices


def ph_bpp(length: Number, width: Number, rectangles: RectList,
           start: Point=(0, 0), sorting: SortAttr='width',
           soft_type: None | SoftType=None,
           excess: Number=0) -> list[Rectangle]:
    """Приоритетная эвристика для задачи упаковки контейнера.

    Учитывает поворот элементов на 90 градусов и гильотинные
    ограничения.

    :param length: Длина контейнера
    :type length: Number
    :param width: Ширина контейнера
    :type width: Number
    :param rectangles: Список прямоугольников
    :type rectangles: RectList
    :param start: Стартовая точка, defaults to (0, 0)
    :type start: Point, optional
    :param sorting: Параметр сортировки, см. :func:`sort`, defaults to 'width'
    :type sorting: SortAttr, optional
    :param soft_type: Мягкие размеры, см. :func:`get_best_fig`, defaults to None
    :type soft_type: None | SoftType, optional
    :param excess: Степень превышения исходных размеров, см. :func:`get_best_gig`, defaults to 0
    :type excess: Number, optional
    :return: Список размещенных элементов
    :rtype: list[Rectangle]
    """
    result = []

    for rect in rectangles:
        if rect.width > rect.length:
            rect.length, rect.width = rect.width, rect.length

    _, sorted_indices = sort(rectangles, sorting=sorting)
    print(f'{sorted_indices = }')

    recursive_packing(
        *start, length, width, rectangles, sorted_indices, result,
        soft_type=soft_type, excess=excess
    )
    return result


def recursive_packing(x: Number, y: Number, length: Number, width: Number,
                      rectangles: RectList, indices: list[int],
                      result: list[Rectangle],
                      soft_type: None | SoftType=None, excess: Number=0):
    """Рекурсивная процедура для приоритетной эвристики

    :param x: Координата x на плоскости
    :type x: Number
    :param y: Координата y на плоскости
    :type y: Number
    :param length: Длина контейнера
    :type length: Number
    :param width: Ширина контейнера
    :type width: Number
    :param rectangles: Список прямоугольников
    :type rectangles: list[RectangleProtocol]
    :param indices: Список индексов отсортированных прямоугольников
    :type indices: list[int]
    :param result: Список размещенных прямоугольников
    :type result: list[Rectangle]
    :param soft_type: Маркер мягких размеров, см. :func:`get_best_fig`,
                      defaults to None
    :type soft_type: None | int, optional
    :param excess: Степень превышения размеров,
                   см. :func:`get_best_fig`, defaults to 0
    :type excess: Number, optional
    """
    priority, orientation, best = get_best_fig(
        length, width, rectangles, indices, soft_type=soft_type, excess=excess
    )

    if priority < 10 and best is not None:
        if orientation == 0:
            omega, d = rectangles[best].width, rectangles[best].length
        else:
            omega, d = rectangles[best].length, rectangles[best].width
        result.append(Rectangle(d, omega, (x, y), name=str(best)))
        indices.remove(best)

        new_length, new_width = length - d, width - omega
        new_x, new_y = x + omega, y + d
        if priority == 2:
            recursive_packing(
                x, new_y, new_length, width, rectangles, indices, result
            )
        elif priority == 3:
            recursive_packing(
                new_x, y, length, new_width, rectangles, indices, result
            )
        elif priority == 4:
            if not indices:
                min_l = min_w = sys.maxsize
            else:
                min_l = min([rectangles[i].length for i in indices])
                min_w = min([rectangles[i].width for i in indices])
                # Because we can rotate:
                min_w = min(min_l, min_w)
                min_l = min_w
            print(min_l, min_w)
            if new_width < min_w:
                recursive_packing(
                    x, new_y, new_length, width, rectangles, indices, result
                )
            elif new_length < min_l:
                recursive_packing(
                    new_x, y, length, new_width, rectangles, indices, result
                )
            elif d < min_w:
                recursive_packing(
                    x, new_y, new_length, omega, rectangles, indices, result
                )
                recursive_packing(
                    new_x, y, length, new_width, rectangles, indices, result
                )
            else:
                recursive_packing(
                    new_x, y, d, new_width, rectangles, indices, result
                )
                recursive_packing(
                    x, new_y, new_length, width, rectangles, indices, result
                )
        elif priority == 7:
            # для мягких размеров по длине
            new_length, new_width = d, width - omega
            recursive_packing(
                new_x, y, new_length, new_width, rectangles, indices, result
            )
        elif priority == 8:
            # для мягких размеров по ширине
            new_length, new_width = length - d, omega
            recursive_packing(
                x, new_y, new_length, new_width, rectangles, indices, result
            )


def get_best_fig(length: Number, width: Number, rectangles: RectList,
                 indices: list[int], soft_type: None | SoftType=None,
                 excess: Number=0) -> tuple[int, int | None, int | None]:
    """Выбор лучшей фигуры для размещения

    Выбор осуществляется на основе приоритета. Приоритет задается каждой
    фигуре в соответствии с вариантами ее размещения. Максимальный
    приоритет 1 будет у фигуры, занимающей всю область. Остальные
    приоритеты присваиваются по правилам:
    - 1  - размеры прямоугольника совпадают с размерами области
    - 2  - ширина совпадает, а длина прямогольника меньше длины контейнера
    - 3  - длина совпадает, а ширина прямогольника меньше ширины контейнера
    - 4  - оба размера прямоугольника меньше размеров контейнера
    - 5  - ширина совпадает, а длина меньше верхней границы
    - 6  - длина совпадает, а ширина меньше верхней границы
    - 7  - длина меньше верхней границы, а ширина меньше ширины контейнера
    - 8  - ширина меньше верхней границы, а длина меньше длины контейнера
    - 9  - оба размера не меньше верхних границ
    - 10 - прямоугольник нельзя разместить

    Приоритеты 5 - 9 работают только при наличии мягких размеров, т.е.
    парметр `soft_type` принимает значения 1, 2 или 3.

    :param length: Длина контейнера
    :type length: Number
    :param width: Ширина контейнера
    :type width: Number
    :param rectangles: Список прямоугольников
    :type rectangles: RectList
    :param indices: Индексы отсортированных прямоугольников
    :type indices: list[int]
    :param soft_type: Маркер мягких размеров. Степень превышения
                      размеров задается параметром `excess`. Возможные
                      значения:
                      - 1 - значения ширины могут быть превышены
                      - 2 - длина может быть превышена
                      - 3 - и длина и ширина могут быть превышены
                      - `None` - опция недоступна, defaults to `None`
    :type soft_type: None | int, optional
    :param excess: Степень превышения размеров. Выступает как
                   коэффициент 1 + `excess` для длины или ширины
                   контейнера, defaults to 0
    :type excess: Number, optional

    :return: Приоритет, ориентация (0 - текущая, 1 - повернуть на 90
             радусов), индекс лучшей фигуры.
    :rtype: tuple[int, int | None, int | None]
    """
    priority, orientation, best = 11, None, None

    max_length, max_width = length, width
    if soft_type in (1, 3) and excess > 0:
        max_length *= 1 + excess
    if soft_type in (2, 3) and excess > 0:
        max_width *= 1 + excess

    for i in indices:
        size = (rectangles[i].length, rectangles[i].width)
        for j in range(1 + rectangles[i].is_rotatable):
            rect_w = size[(1 + j) % 2]
            rect_l = size[(0 + j) % 2]
            if priority > 1 and rect_l == length and rect_w == width:
                priority, orientation, best = 1, j, i
            elif priority > 2 and rect_l < length and rect_w == width:
                priority, orientation, best = 2, j, i
            elif priority > 3 and rect_l == length and rect_w < width:
                priority, orientation, best = 3, j, i
            elif priority > 4 and rect_l < length and rect_w < width:
                priority, orientation, best = 4, j, i

            # Мягкие размеры
            elif priority > 5 and soft_type and rect_l <= max_length and rect_w == width:
                # Превышение верхней границы (совпадает по ширине)
                priority, orientation, best = 5, j, i
            elif priority > 6 and soft_type and rect_l == length and rect_w <= max_width:
                # Превышение правой границы (совпадает по длине)
                priority, orientation, best = 6, j, i
            elif priority > 7 and soft_type and rect_l <= max_length and rect_w < width:
                # Превышение верхней границы
                priority, orientation, best = 7, j, i
            elif priority > 8 and soft_type and rect_l < length and rect_w <= max_width:
                # Превышение правой границы
                priority, orientation, best = 8, j, i

            # выход за обе границы
            elif priority > 9 and soft_type and rect_l <= max_length and rect_w <= max_width:
                priority, orientation, best = 9, j, i
            elif priority > 10:
                priority, orientation, best = 10, j, i
    return priority, orientation, best
