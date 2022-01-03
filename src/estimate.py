"""Модуль оценки доступных размеров"""

from .types import Number


def estimate_size(length: Number, width: Number, height: Number,
                  roll_height: Number,
                  x: Number, y: Number) -> tuple[Number, Number]:
    """Оценка доступных размеров

    Оценка проводится по правилу сохранения объема.
    Нижний левый угол исходного контейнера располагается в начале
    координат, в точке (0, 0).

    :param length: Длина исходного контейнера
    :type length: Number
    :param width: Ширина исходного контейнера
    :type width: Number
    :param height: Толщина исходного контейнера
    :type height: Number
    :param roll_height: Толщина проката, целевая толщина
    :type roll_height: Number
    :param x: Координата точки по оси X для которой происходит оценивание
    :type x: Number
    :param y: Координата точки по оси Y для которой происходит оценивание
    :type y: Number
    :raises ValueError: При отрицательных значениям аргумента `x`
    :raises ValueError: При отрицательных значениям аргумента `y`
    :raises ValueError: При выходе точки (`x`, `y`) за границы области
    :raises ValueError: При выходе точки (`x`, `y`) за границы области
                        в криволинейной части
    :return: Доступное расстояние по обеим осям
    :rtype: tuple[Number, Number]
    """
    max_length = length * height / roll_height
    max_width = width * height / roll_height
    x_estimate = y_estimate = None

    if x < 0:
        raise ValueError('Значение x должно быть >= 0')
    if y < 0:
        raise ValueError('Значение y должно быть >= 0')

    if 0 <= x <= width and 0 <= y <= length:
        # внутренний прямоугольник
        x_estimate = max_width
        y_estimate = max_length
    if 0 <= x <= width and length < y <= max_length:
        # верхний левый прямоугольник
        temp_height = length * height / y
        x_estimate = width * temp_height / roll_height
        y_estimate = max_length
    if width < x <= max_width and 0 <= y <= length:
        # нижний правый прямоугольник
        temp_height = width * height / x
        x_estimate = max_width
        y_estimate = length * temp_height / roll_height
    if width < x <= max_width and length < y <= max_length:
        # верхний правый прямоугольник
        temp_height_x = width * height / x
        temp_height_y = length * height / y
        x_estimate = width * temp_height_y / roll_height
        y_estimate = length * temp_height_x / roll_height

    if x_estimate is None or y_estimate is None:
        raise ValueError(
            f'Ошибка оценки расстояний. Точка {(x, y)} выходит за '
            f'допустимые границы {(max_length, max_width)}'
        )

    x_estimate -= x
    y_estimate -= y

    if x_estimate < 0 or y_estimate < 0:
        raise ValueError(
            f'Ошибка оценки расстояний. Точка {(x, y)} выходит за '
            'допустимые границы криволинейной области'
        )

    return x_estimate, y_estimate
