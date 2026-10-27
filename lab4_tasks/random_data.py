"""Генераторы случайных чисел и записей."""

from collections.abc import Iterator
from itertools import count
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


def random_records(
    *, seed: int | None = None
) -> Iterator[dict[str, int | str]]:
    """Бесконечно выдавать записи id, category и value.

    id начинается с 1, category выбирается из A/B/C, value — целое
    число от 0 до 100 включительно. Каждая запись — новый словарь.
    Для конечной выборки используйте itertools.islice.
    """
    if seed is not None:
        require_integer(seed, "Seed")
    generator = Random(seed)
    for identifier in count(1):
        yield {
            "id": identifier,
            "category": generator.choice(("A", "B", "C")),
            "value": generator.randint(0, 100),
        }
