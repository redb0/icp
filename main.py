"""Модуль с примерами использования библиотеки"""

from problem import Problem
from src.algorithm import create_rectangles, algorithm_wl
from src.visualize import visualize


EXAMPLES = [
    [(5, 5), (5, 1), (1, 6), (1, 6), (1, 7), (1, 7), (2, 8), (1, 9)],
    [(6, 2), (2, 3), (1, 2), (2, 2)],
    [(5, 3), (5, 3), (2, 4), (30, 8), (10, 20)],
    [(20, 10), (5, 5), (5, 5), (10, 10), (10, 5)],
    [(6, 4), (1, 10), (8, 4), (6, 6), (20, 14)],
    [
        (20, 25), (20, 15), (15, 15), (5, 15), (10, 20), (10, 15),
        (5, 20), (5, 10), (5, 10), (15, 30), (5, 25), (10, 25),
    ]
]


def int_input(msg: str) -> int:
    """Ввод целого числа"""
    while (user_input := input(msg)) and user_input != 'q':
        try:
            return int(user_input)
        except ValueError:
            print('Повторите ввод.')
    return -1


def print_simple_stats(number_rectangles, placed, min_rect):
    """Вывод простой статистики"""
    efficiency = sum(item.area for item in placed) / min_rect.area
    print('-' * 50)
    print(f'Количество прямоугольников: {number_rectangles}')
    print(
        f'Упаковано: {len(placed)} из {number_rectangles}'
        f' ({len(placed) / number_rectangles})'
    )
    print(f'Размеры контейнера: {min_rect.length}х{min_rect.width}')
    print(f'Эффективность: {efficiency}')
    print('-' * 50)


def simple_example():
    """Простые примеры алгоритма без ограничений"""
    msg = (
        f'Введите номер примера от 0 до {len(EXAMPLES) - 1} или q для выхода: '
    )
    number = int_input(msg)
    if not 0 <= number < len(EXAMPLES):
        print(f'Примера с номером {number} не существует.')
        return

    rectangles = create_rectangles(EXAMPLES[number])

    print(f'Пример №{number}, сортировка по площади')
    placed, min_rect = algorithm_wl(rectangles, sorting='area')

    print_simple_stats(len(rectangles), placed, min_rect)

    visualize(min_rect.length, min_rect.width, placed)


def zdf_dataset():
    """Запуск примеров из датасета zdf"""
    msg = 'Введите номер примера от 1 до 16 или q для выхода: '
    number = int_input(msg)
    if not 1 <= number <= 16:
        print(f'Примера с номером {number} не существует.')
        return

    path = f'datasets/zdf/zdf{number}.txt'
    problem = Problem.read(path)
    print(f'Пример: {path}')

    rectangles = create_rectangles(problem.rectangles)
    placed, min_rect = algorithm_wl(rectangles, sorting='area')

    print_simple_stats(len(rectangles), placed, min_rect)

    visualize(min_rect.length, min_rect.width, placed)


def main():
    """Примеры работы алгоритма"""
    msg = 'Использовать простые примеры [y] или zdf [n]? y/n '
    positive = 'y', 'yes'
    valid = (*positive, 'n', 'no')
    while (user_input := input(msg).lower()) and user_input not in valid:
        pass

    if user_input in positive:
        simple_example()
    else:
        main()


if __name__ == '__main__':
    main()
