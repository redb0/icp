"""Модуль вспомогательных функций"""

import time
import logging
import logging.config
from functools import wraps


def timeit(func):
    """Таймер времени выполнения функции

    :param func: функция, время выполнения которой измеряется
    :type func: Collable
    """
    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.time()
            print(f'\033[31mTime {func.__name__}: {end - start} sec\033[0m')
            logging.info(
                'Время выполнения функции %(name)s: '
                '%(time).4f сек', {'name': func.__name__, 'time': end - start}
            )
    return inner
