"""Среднее задание №3: сумма чисел через functools.reduce."""

from collections.abc import Iterable
from functools import reduce
from operator import add

from .validation import Number, require_number


def sum_with_reduce(numbers: Iterable[Number]) -> Number:
    """Сложить числа за один проход; для пустого входа вернуть 0."""
    checked = (require_number(number) for number in numbers)
    result = reduce(add, checked, 0)
    return require_number(result)
