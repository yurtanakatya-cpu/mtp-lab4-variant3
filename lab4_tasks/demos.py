"""Короткие конечные демонстрации всех пяти заданий."""

import json
from itertools import islice

from .currying import curry
from .fibonacci import fibonacci_numbers
from .random_data import random_numbers, random_records
from .reduction import sum_with_reduce


def show_demos() -> None:
    """Показать свёртку, генераторы и каррирование."""
    print("--- sum ---")
    print(sum_with_reduce([1, 2, 3, 4, 5]))

    print("--- fibonacci ---")
    print(*islice(fibonacci_numbers(), 8))

    print("--- random ---")
    print(*random_numbers(1, 10, 5, seed=42))

    print("--- curry ---")
    multiply = curry(lambda a, b, c: a * b * c)
    times_two = multiply(2)
    print("2 × 3 × 4 =", times_two(3)(4))
    print("2 × 5 × 6 =", times_two(5)(6))

    print("--- records ---")
    for record in islice(random_records(seed=42), 3):
        print(json.dumps(record, ensure_ascii=False))
