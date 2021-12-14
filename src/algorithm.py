"""Модуль эвристики для задачи упаковки в минимальный прямоугольник

Содержит реализации алгоритмов:
- Эвристику максимального прироста полезной площади
для неограниченной задачи
- Эвристику максимального прироста полезной площади
для ограниченной задачи проката слитка
"""

from operator import attrgetter, itemgetter
from dataclasses import dataclass
from typing import Literal, TypeAlias

from .utils import timeit
from .ph import ph_bpp
from .types import Number, SizeList, Coord, SoftType
from .base import Rectangle, min_enclosing_rect, difference_rect


SortingOptions: TypeAlias = Literal['length', 'width', 'area', 'diagonal']
RotateOptions: TypeAlias = Literal['length', 'width']
ListRectangles: TypeAlias = list[Rectangle]


@dataclass
class LocationOption:
    """Представление решения для области

    :param size_list: Список пар из размещенного прямоугольника и индекса
    :param min_rect: Минимальный объемлющий прямоугольник
    :param efficiency: Эффективность
    """
    placed: list[tuple[Rectangle, int]]
    min_rect: Rectangle
    efficiency: Number


def create_rectangles(size_list: SizeList) -> ListRectangles:
    """Создание списка прямоугольников

    :param size_list: Список размеров в виде пар (длина, ширина)
    :type size_list: SizeList
    :return: Список экземпляров класса Rectangle
    :rtype: list[Rectangle]
    """
    return [Rectangle(*size) for size in size_list]


def sort_rect(rectangles: ListRectangles,
              sorting: SortingOptions='length') -> ListRectangles:
    """Сортировка прямоугольников по невозрастанию

    Сортировка может выполняться по параметрам:
    - длине `sorting='length'`
    - ширине `sorting='width'`
    - площади `sorting='area'`

    :param rectangles: Список прямоугольников
    :type rectangles: ListRectangles
    :param sorting: Параметр сортировки, defaults to 'length'
    :type sorting: SortingOptions, optional
    :return: Отсортированный по невозрастанию список прямоугольников
    :rtype: ListRectangles
    """
    return sorted(rectangles, key=attrgetter(sorting), reverse=True)


def rotate_all(rectangles: ListRectangles, rtype: RotateOptions) -> None:
    """Поворот прямоугольников

    Поворот осуществляется таким образом, чтобы максимальная сторона
    стала длиной (`rtype='length'`) или шириной (`rtype='width'`).

    :param rectangles: Список прямоугольников
    :type rectangles: ListRectangles
    :param rtype: Параметр вращения
    :type rtype: RotateOptions
    """
    for rect in rectangles:
        max_side, min_side = max(rect.size), min(rect.size)
        if rtype == 'width':
            rect.size = min_side, max_side
        else:
            rect.size = max_side, min_side


def soft_size_type(rect: Rectangle,
                   min_rect: Rectangle) -> SoftType | None:
    """Определение типа "мягких" размеров

    Мягкие размеры допустимы только если у прямоугольника свободна
    правая (1) или верхняя (2) стороны или обе одновременно (3).

    :return: Тип мягких размеров. 1, 2 или 3 если расширение допустимо,
             иначе `None`
    :rtype: SoftType | None
    """
    is_right = rect.brp[0] == min_rect.brp[0]
    is_top = rect.trp[1] == min_rect.trp[1]
    if is_right and is_top:
        # расширение в любую сторону
        return 3
    if is_right and not is_top:
        # расширение по ширине
        return 1
    if not is_right and is_top:
        # расширение по длине
        return 2
    # нельзя расширять
    return None


@timeit
def get_best_fig(rectangles: ListRectangles, indices: list[int], region: Coord,
                 min_rect: Rectangle) -> tuple[int | None, int, Rectangle | None, list[tuple[Rectangle, int]]]:
    """Выбор лучшего варианта размещения

    Выбор осуществляется на основе вычисления свободного прямоугольника
    порождаемого предыдущим объемлющим прямоугольников и размещаемым
    элементов. Для пустой области решается меньшая задача упаковки.
    Выбор происходит по итоговой эффективности и площади нового
    объемлющего прямоугольника. Сравнение в первую очередь происходит
    по эффективности (доле полезной площади). Для вариантов с одинаковой
    эффективностью выбирается тот, площадь объемлющего прямоугольника у
    которого больше.

    :return: Набор параметров нового размещения. Состоит из:
             - индекса прямоугольника, породившего размещение
             - ориентации (0 или 1)
             - нового объемлющего прямоугольника
             - набора пар (прямоугольник, индекс) упаковки свободного
             пространства, включает прямоугольник, породивший упаковку
    :rtype: tuple[int | None, int, Rectangle | None, list[tuple[Rectangle, int]]]
    """
    best, orientation, max_ef, max_area, res_min_rect = None, 0, 0, 0, None
    best_res = []
    viewed = set()
    for index in indices:
        is_first = min_rect.area == 0
        rect = rectangles[index]
        size = (rect.length, rect.width)
        if size not in viewed:
            viewed.add(size)
        else:
            continue
        rotate_variants = []
        # k = 0
        for j in range(1 + rect.is_rotatable):
            rect_length = rect.size[(0 + j) % 2]
            rect_width = rect.size[(1 + j) % 2]

            new_min_rect = min_enclosing_rect(
                [Rectangle(rect_length, rect_width, region), min_rect]
            )
            best_rect = rectangles[index].copy()
            if j == 1:
                best_rect.rotate()
            best_rect.coord = region
            if new_min_rect.area <= max_area and max_ef == 1:
                continue
            empty = difference_rect(new_min_rect, [min_rect, best_rect])
            best_idx = indices.index(index)
            remainder = indices[:best_idx] + indices[best_idx + 1:]
            soft_type = None
            # if empty:
            #     soft_type = soft_size_type(empty[0], min_rect)
            res = additional_packaging(empty, rectangles, remainder, soft_type)
            res.append((best_rect, index))
            max_length = max([item.tlp[1] for item, _ in res])
            max_width = max([item.brp[0] for item, _ in res])
            if max_length > new_min_rect.length:
                new_min_rect.length = max_length
            if max_width > new_min_rect.width:
                new_min_rect.width = max_width

            area = sum([r.area for r, _ in res])
            efficiency = (area + min_rect.area) / new_min_rect.area

            rotate_variants.append(
                (efficiency, new_min_rect.area, j, index, new_min_rect, res)
            )
        if rotate_variants:
            if best is None:
                max_ef, max_area, orientation, best, res_min_rect, best_res = max(
                    rotate_variants, key=itemgetter(0, 1)
                )
            else:
                candidate_ef, candidate_area, candidate_or, candidate, candidate_min_rect, candidate_res = max(
                    rotate_variants, key=itemgetter(0, 1)
                )
                if len(indices) == len(best_res) > len(candidate_res):
                    continue
                if (candidate_ef, candidate_area) > (max_ef, max_area):
                    orientation = candidate_or
                    max_ef, best = candidate_ef, candidate
                    max_area = candidate_area
                    res_min_rect = candidate_min_rect
                    best_res = candidate_res
        if is_first:
            break
    return best, orientation, res_min_rect, best_res


def additional_packaging(min_rect, rectangles, indices: list[int], soft_type):
    """Доупаковка свободного пространства"""
    result = []
    if min_rect:
        if len(min_rect) == 1:
            min_rect = min_rect[0]
        else:
            raise ValueError('Что-то пошло не так!')
        res = ph_bpp(
            min_rect.length, min_rect.width, [rectangles[i] for i in indices],
            start=min_rect.blp, soft_type=soft_type, excess=0.2
        )
        for i, item in res:
            result.append((item, indices[i]))
    return result


@timeit
def algorithm_wl(rectangles, sorting='length', rtype='width'):
    # без ограничений
    if sorting not in ('length', 'width', 'area', 'diagonal'):
        raise ValueError(
            'Rectangles can only be sorted by length, width, area, or '
            f'diagonal but {sorting} was given.'
        )
    if rtype not in ('width', 'length'):
        raise ValueError(
            'Long side of rectangle can be length or width '
            f'but {rtype} was given.'
        )
    # rotate_all(rectangles, rtype)
    rectangles = sort_rect(rectangles, sorting)
    indices = list(range(len(rectangles)))

    start = (0, 0)
    min_rect = Rectangle(0, 0)
    placed = []
    regions = [start]

    k = 0

    while indices:
        k += 1
        layouts = []
        for region in regions:
            # выбрать лучшую заготовку
            # считаем объемлющий прямоугольник
            best, _, new_min_rect, best_res = get_best_fig(
                rectangles, indices, region, min_rect
            )
            if best is None or new_min_rect is None:
                raise ValueError()

            best_rect = best_res[-1][0]
            max_length = max([item.tlp[1] for item, _ in best_res])
            max_width = max([item.brp[0] for item, _ in best_res])
            if max_length > new_min_rect.length:
                new_min_rect.length = max_length
            if max_width > new_min_rect.width:
                new_min_rect.width = max_width
            # если есть, доупаковываем с мягкими размерами
            # считаем эффективность этого варианта
            if min_rect.area == 0:
                efficiency = best_rect.area / new_min_rect.area
            else:
                fig_area = sum([rect.area for rect, _ in best_res])
                efficiency = (min_rect.area + fig_area) / new_min_rect.area
            # сохраняем вариант
            layouts.append(
                LocationOption(
                    best_res, new_min_rect, efficiency
                )
            )
        # выбираем лучший вариант
        layout = max(
            enumerate(layouts),
            key=lambda item: (item[1].efficiency, sum([r[0].area for r in item[1].placed]))
        )
        layout = layout[1]
        # обновляем упакованные заготовки
        for rect, src in layout.placed:
            placed.append(rect)
            indices.remove(src)
        # обновляем объемлющий прямоугольник
        min_rect = layout.min_rect
        # вычисляем новые регионы
        regions = [min_rect.tlp, min_rect.brp]
        # print(f'Новые регионы: {regions = }')
        # visualize(min_rect.length, min_rect.width, placed)
        print(f'Шаг {k}: {len(placed)}')

    return placed, min_rect
