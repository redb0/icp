"""Модуль для визуализации вспомогательных графиков

Предназначен для исследования различных аспектов решаемых задач раскроя.
"""

from typing import TypeAlias

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Rectangle


Number: TypeAlias = int | float


rcParams['text.usetex'] = True
rcParams['font.family'] = 'serif'
rcParams['font.sans-serif'] = ['Times New Roman']
rcParams['font.size'] = '14'


def remove_border(axis):
    """Удаление верхней и правой границы"""
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)


def graph_size_restrictions(length: Number, width: Number,
                            height: Number, roll_height: Number) -> None:
    """График возможных размеров после проката

    Прокат происходит и по вертикали и по горизонтали. Новые размеры
    зависят от начальных размеров и конечной толщины листа. Новые
    размеры определяются по правилу сохранения объема. При прокате
    только по вертикали или только по горизонтали соответствующая
    сторона просто пропорционально увеличивается.

    :param length: Длина исходного листа
    :type length: Number
    :param width: Ширина исходного листа
    :type width: Number
    :param height: Толщина исходного листа
    :type height: Number
    :param roll_height: Толщина до которой следует прокатать лист
    :type roll_height: Number
    """
    _, axis = plt.subplots(1, 1)

    remove_border(axis)

    # axis.plot(
    #     1, 0, ">k", transform=axis.get_yaxis_transform(), clip_on=False
    # )
    # axis.plot(
    #     0, 1, "^k", transform=axis.get_xaxis_transform(), clip_on=False
    # )

    # исходный прямоугольник
    axis.add_patch(
        Rectangle(
            (0, 0), width, length, fill=False,
            linestyle='-', linewidth=1
        )
    )

    volume = length * width * height
    max_length = length * height / roll_height
    max_width = width * height / roll_height

    # координаты линии ограничения
    xs: list[Number] = []
    start = width
    while start < max_width:
        xs.append(start)
        start += 0.1
    xs.append(max_width)

    # границы графика
    x_lim, y_lim = int(3 * width), int(2.5 * length)

    axis.vlines(
        x=max_width, ymin=0, ymax=length,
        linestyles='solid', linewidth=1
    )
    axis.vlines(
        x=width, ymin=length, ymax=max_length,
        colors='k', linestyles='dashed', linewidth=1
    )
    axis.hlines(
        y=max_length, xmin=0, xmax=width,
        linestyles='solid', linewidth=1
    )
    axis.hlines(
        y=length, xmin=width, xmax=max_width,
        colors='k', linestyles='dashed', linewidth=1
    )
    axis.plot(xs, [volume / (x * roll_height) for x in xs], linewidth=1)

    # подписи меток на осях
    axis.set_xticks([0, width, max_width, x_lim])
    axis.set_xticklabels(
        ['$0$', '$W_0$', '$W_{max}=\\frac{H_0L_0}{H_1}$', '$x$']
    )
    axis.set_yticks([0, length, max_length, y_lim])
    axis.set_yticklabels(
        ['$0$', '$L_0$', '$L_{max}=\\frac{H_0W_0}{W_1}$', '$y$']
    )

    axis.set_xlim(0, x_lim)
    axis.set_ylim(0, y_lim)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


if __name__ == '__main__':
    graph_size_restrictions(10, 6, 3, 1.5)
