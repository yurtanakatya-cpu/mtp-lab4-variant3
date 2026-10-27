"""Среднее задание №5: генератор чисел Фибоначчи."""

from collections.abc import Iterator


def fibonacci_numbers() -> Iterator[int]:
    """Лениво выдавать 0, 1, 1, 2, 3, ... без ограничения длины."""
    first, second = 0, 1
    while True:
        yield first
        first, second = second, first + second
