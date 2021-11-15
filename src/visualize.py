"""Модуль визуализации схемы раскроя

:Date: 14.11.2021
:Version: 0.1
:Authors:
    - Воронов Владимир Сергеевич
"""

from random import uniform

import matplotlib.pyplot as plt
import matplotlib.patches as ptc


def patch_rect(axis, point, width, length, **kwargs):
    """Создание прямоугольника

    :param axis: ось
    :type axis: matplotlib.axes._subplots.AxesSubplot
    :param point: опорная точка (левый нижний угол)
    :type point: tuple[Number, Number]
    :param width: ширина прямоугольника
    :type width: int или float
    :param length: высота прямоугольника
    :type length: int или float
    """
    obj = axis.add_patch(
        ptc.Rectangle(point, width, length, **kwargs)
    )
    return obj


def visualize(length, width, rectangles, title='', with_label=False):
    """Визуализация схемы раскроя

    :param length: Длина контейнера
    :type length: int | float
    :param width: Ширина контейнера
    :type width: int | float
    :param rectangles: Список прямоугольников
    :type rectangles: list[Rectangle]
    :param title: Заголовок, defaults to ''
    :type title: str, optional
    :param with_label: Маркер подписей прямоугольников, defaults to False
    :type with_label: bool, optional
    """
    _, axes = plt.subplots()
    axes.set_xlim([0, int(width * 1.15)])
    axes.set_ylim([0, int(length * 1.15)])
    axes.set_title(title)

    patch_rect(
        axes, (0, 0), width, length,
        color='k', hatch='x', fill=False, ec='k', lw=1
    )
    for rect in rectangles:
        # Прямоугольник с заливкой
        patch_rect(
            axes, (rect.x, rect.y), rect.width, rect.length,
            color=(uniform(0.5, 1), uniform(0.5, 1), uniform(0.5, 1)),
            ec='k', lw=0.5
        )
        # Прямоугольник с контуром
        patch_rect(
            axes, (rect.x, rect.y), rect.width, rect.length,
            color='k', fill=False, ec='k', lw=1
        )
        if with_label:
            axes.text(
                rect.x + 0.5 * rect.width, rect.y + 0.5 * rect.length,
                rect.name
            )
    plt.show()
