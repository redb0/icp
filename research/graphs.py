"""Модуль для визуализации вспомогательных графиков

Предназначен для исследования различных аспектов решаемых задач раскроя.
"""

import math
from typing import TypeAlias
from pathlib import Path
from statistics import mean, stdev, median

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


def graph_aspect_ratio_efficiency():
    efficiency = []
    aspect_ratio_std = []
    gaps = []

    abs_path = Path.cwd()
    res_file = abs_path / 'results/zdf_area_result.txt'
    zdf_path = abs_path / 'datasets/zdf'
    with res_file.open('r', encoding='utf-8') as file:
        for i, line in enumerate(file.readlines()):
            if i == 2 or (i - 2) % 4 == 0:
                efficiency.append(float(line))
            if i == 1 or (i - 1) % 4 == 0:
                gaps.append(math.prod([int(item) for item in line.split()]))

    for i in range(1, 16 + 1):
        example_path = zdf_path / f'zdf{i}.txt'
        print(f'{example_path = }')
        aspect_ratio = []
        length = width = 0
        with example_path.open('r', encoding='utf-8') as file:
            for j, line in enumerate(file.readlines()):
                if j == 1:
                    length = int(line)
                elif j == 2:
                    width = int(line)
                elif j > 2:
                    size = [int(item) for item in line.split()]
                    aspect_ratio.append(max(size) / min(size))
                    # Площадь
                    # aspect_ratio.append((length * width) / (size[0] * size[1]))
                    # aspect_ratio.append((size[0] * size[1]) / (length * width))
                    # aspect_ratio.append(size[0] * size[1])
                    # Пропорции
                    # aspect_ratio.append(
                    #     (max((length, width)) / min((length, width))) / (max(size) / min(size))
                    # )
        gaps[i - 1] = (gaps[i - 1] - (length * width)) / (length * width)
        aspect_ratio_std.append(stdev(aspect_ratio))

        print(f'zdf{i} mean: {mean(aspect_ratio)}')
        print(f'zdf{i} median: {median(sorted(aspect_ratio))}')
        print(f'Gap: {gaps[i - 1]}')
        print('-' * 50)

    print(f'Min aspect ratio std: {min(aspect_ratio_std)}')
    print(f'Max aspect ratio std: {max(aspect_ratio_std)}')
    print(f'Mean aspect ratio std: {mean(aspect_ratio_std)}')

    print(f'Min gap: {min(gaps)}')
    print(f'Max gap: {max(gaps)}')
    print(f'Mean gap: {mean(gaps)}')

    _, axes = plt.subplots(figsize=(12, 6))
    axes.grid()
    for i, (x, y) in enumerate(zip(aspect_ratio_std, efficiency)):
        axes.scatter(x, y, color="black")
        if i == 4:
            axes.annotate(f'zdf{i + 1}', xy=(x, y), xytext=(x - 1.04, y - .0013))
        elif i == 7:
            axes.annotate(f'zdf{i + 1}', xy=(x, y), xytext=(x - 1.04, y - .0013))
        elif i == 9:
            axes.annotate(f'zdf{i + 1}', xy=(x, y), xytext=(x - 1.08, y - .0013))
        elif i == 15:
            axes.annotate(f'zdf{i + 1}', xy=(x, y), xytext=(x - 1.08, y - .0013))
        else:
            axes.annotate(f'zdf{i + 1}', xy=(x, y), xytext=(x + .15, y - .0013))
    axes.set_xlabel('$\sigma_a$')
    axes.set_ylabel('$f(S)$', rotation=0)
    plt.show()


if __name__ == '__main__':
    # graph_size_restrictions(10, 6, 3, 1.5)
    graph_aspect_ratio_efficiency()
