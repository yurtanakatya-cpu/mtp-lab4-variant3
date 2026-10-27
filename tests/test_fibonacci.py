"""Проверки ленивого генератора Фибоначчи."""

import unittest
from itertools import islice
from types import GeneratorType

from lab4_tasks.fibonacci import fibonacci_numbers


class FibonacciTests(unittest.TestCase):
    def test_first_ten_values(self) -> None:
        self.assertEqual(
            list(islice(fibonacci_numbers(), 10)),
            [0, 1, 1, 2, 3, 5, 8, 13, 21, 34],
        )

    def test_returns_generator(self) -> None:
        self.assertIsInstance(fibonacci_numbers(), GeneratorType)

    def test_resumes_after_partial_consumption(self) -> None:
        numbers = fibonacci_numbers()
        self.assertEqual(list(islice(numbers, 5)), [0, 1, 1, 2, 3])
        self.assertEqual(list(islice(numbers, 3)), [5, 8, 13])

    def test_instances_are_independent(self) -> None:
        first = fibonacci_numbers()
        second = fibonacci_numbers()
        next(first)
        next(first)
        self.assertEqual(next(second), 0)
        self.assertEqual(next(first), 1)

    def test_long_sequence_without_recursion(self) -> None:
        values = list(islice(fibonacci_numbers(), 2000))
        self.assertEqual(len(values), 2000)
        self.assertEqual(values[-1], values[-2] + values[-3])


if __name__ == "__main__":
    unittest.main()
