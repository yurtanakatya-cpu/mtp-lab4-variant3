"""Генераторы случайных чисел и записей."""

from collections.abc import Iterator
from random import Random

from .validation import require_count, require_integer


def random_numbers(
    lower: int, upper: int, count: int, *, seed: int | None = None
) -> Iterator[int]:
    """Выдать count целых чисел в [lower, upper], включая обе границы."""
    require_integer(lower, "Нижняя граница")
    require_integer(upper, "Верхняя граница")
    require_count(count)
    if lower > upper:
        raise ValueError("Нижняя граница не должна превышать верхнюю")
    if seed is not None:
        require_integer(seed, "Seed")
    generator = Random(seed)
    for _ in range(count):
        yield generator.randint(lower, upper)
