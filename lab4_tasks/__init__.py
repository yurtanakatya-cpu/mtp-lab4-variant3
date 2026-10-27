"""Функции и генераторы лабораторной работы №4."""

from .currying import curry
from .fibonacci import fibonacci_numbers
from .random_data import random_numbers, random_records
from .reduction import sum_with_reduce

__all__ = [
    "curry",
    "fibonacci_numbers",
    "random_numbers",
    "random_records",
    "sum_with_reduce",
]
