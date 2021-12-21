"""Модуль для работы с примером"""

import math
from pathlib import Path
from statistics import mean, stdev
from typing import TypeAlias


Number: TypeAlias = int | float
Size: TypeAlias = tuple[Number, Number]
ListSize: TypeAlias = list[Size]


class Problem:
    """Экземпляр задачи упаковки"""
    def __init__(self, size: Size, rectangles: ListSize, name='') -> None:
        self.name = name
        self._size = size
        self._rectangles = rectangles

    def to_dict(self) -> dict[str, str | Number | ListSize]:
        """Преобразование в словарь

        :return: Словарь с параметрами задачи
        :rtype: dict[str, str | Number | ListSize]
        """
        return {
            'name': self.name,
            'bin_length': self._size[0],
            'bin_width': self._size[1],
            'rectangles': self._rectangles
        }

    def save(self, path: str='') -> None:
        """Сохранение в файл формата txt

        :param path: Путь до файла
        :type path: str
        """
        if path:
            abs_path = path
        elif self.name:
            abs_path = Path.cwd() / f'./datasets/{self.name}.txt'
        else:
            raise ValueError('File path or problem name not specified')
        save(self._rectangles, *self._size, abs_path)

    @classmethod
    def read(cls, path: str) -> 'Problem':
        """Загрузка примера из txt файла

        :return: Экземпляр класса примера
        :rtype: Problem
        """
        length, width, rectangles = read(path)
        return cls((length, width), rectangles, name=str(path))

    def spec_area(self) -> dict[str, Number]:
        """Характеристики, связанные с площадью

        :return: Словарь с характеристиками
        :rtype: dict[str, Number]
        """
        areas = [math.prod(size) for size in self._rectangles]
        barea_ratio = [
            math.prod(size) / math.prod(self._size) for size in self._rectangles
        ]
        return {
            'area': self._size[0] * self._size[1],
            'max_area': max(areas),  # Максимальная площадь
            'min_area': min(areas),  # Минимальная площадь
            'mean_area': mean(areas),  # Средняя площадь
            'std_area': stdev(areas),  # Средняя площадь
            'max_barea_ratio': max(barea_ratio),
            'min_barea_ratio': min(barea_ratio),
            'mean_barea_ratio': mean(barea_ratio),
            'std_barea_ratio': stdev(barea_ratio),
            'max_area_ratio': max(areas) / min(areas),  # максимальное соотношение площадей
        }

    def spec_proportion(self) -> dict[str, Number]:
        """Характеристики, связанные с пропорциями

        :return: Словарь с характеристиками
        :rtype: dict[str, Number]
        """
        aspect_ratio = [
            max(size) / min(size) for size in self._rectangles
        ]
        bin_aspect_ratio = max(self._size) / min(self._size)
        baspect_ratio = [
            bin_aspect_ratio / (max(size) / min(size)) for size in self._rectangles
        ]

        return {
            'bin_aspect_ratio': bin_aspect_ratio,  # Соотношение сторон
            'max_aspect_ratio': max(aspect_ratio),  # Максимальное соотношение сторон
            'min_aspect_ratio': min(aspect_ratio),  # Минимальное соотношение сторон
            'mean_aspect_ratio': mean(aspect_ratio),  # Среднее соотношение сторон
            'std_aspect_ratio': stdev(aspect_ratio),

            'max_baspect_ratio': max(baspect_ratio),
            'min_baspect_ratio': min(baspect_ratio),
            'mean_baspect_ratio': mean(baspect_ratio),
            'std_baspect_ratio': stdev(baspect_ratio),
        }

    def print_spec_area(self) -> None:
        """Печать характеристик площади"""
        print(f'Параметры площади примера {self.name}:')
        for key, value in self.spec_area().items():
            print(f'\t{key}: {value:.6f}')
        print('-' * 50)

    def print_spec_proportion(self) -> None:
        """Печать характеристик пропорций"""
        print(f'Параметры пропорций примера {self.name}:')
        for key, value in self.spec_proportion().items():
            print(f'\t{key}: {value:.6f}')
        print('-' * 50)

    @property
    def rectangles(self) -> ListSize:
        """Список размеров прямоугольников"""
        return self._rectangles

    @property
    def size(self) -> Size:
        """Размеры контейнера в виде пары (длина, ширина)"""
        return self._size

    def __len__(self) -> int:
        return len(self._rectangles)

    def __str__(self) -> str:
        return (
            f'Problem {self.name} with '
            f'{self.__len__()} rectangles and size {self._size}'
        )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}'
            f'({self._size}, {self._rectangles}, name={self.name})'
        )


def read(path: str) -> tuple[Number, Number, ListSize]:
    """Чтение примера из txt файла

    :param path: Путь до файла
    :type path: str
    :return: Длина, ширина контейнера и список размеров прямоугольников
    :rtype: tuple[Number, Number, ListSize]
    """
    rectangles = []
    bin_length = bin_width = 0
    with open(path, mode='r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i == 0:
                continue
                # count = int(line)
            if i == 1:
                bin_width = int(line)
            elif i == 2:
                bin_length = int(line)
            else:
                length, width = map(int, line.split())
                rectangles.append((length, width))
    return bin_length, bin_width, rectangles


def save(rectangles: ListSize,
         bin_length: Number, bin_width: Number, path: str | Path) -> None:
    """Сохранение примера в текстовый файл

    :param rectangles: Список размеров прямоугольников
    :type rectangles: ListSize
    :param bin_length: Длина контейнера
    :type bin_length: Number
    :param bin_width: Ширина контейнера
    :type bin_width: Number
    :param path: Путь до файла
    :type path: str
    """
    with open(path, mode='w', encoding='utf-8') as file:
        file.write(f'{len(rectangles)}\n')
        file.write(f'{bin_width}\n')
        file.write(f'{bin_length}\n')
        for rect in rectangles:
            file.write(f'{rect[0]} {rect[1]}\n')
