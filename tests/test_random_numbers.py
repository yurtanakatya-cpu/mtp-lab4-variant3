"""Проверки диапазона, воспроизводимости и состояния генератора."""

import random
import unittest
from itertools import islice
from types import GeneratorType

from lab4_tasks.random_data import random_numbers


class RandomNumbersTests(unittest.TestCase):
    def test_count_and_inclusive_range(self) -> None:
        numbers = list(random_numbers(-3, 7, 100, seed=42))
        self.assertEqual(len(numbers), 100)
        self.assertTrue(all(-3 <= number <= 7 for number in numbers))
        self.assertTrue(all(type(number) is int for number in numbers))

    def test_equal_boundaries(self) -> None:
        self.assertEqual(list(random_numbers(5, 5, 3)), [5, 5, 5])

    def test_zero_count(self) -> None:
        self.assertEqual(list(random_numbers(1, 10, 0)), [])

    def test_same_seed_reproduces_sequence(self) -> None:
        self.assertEqual(
            list(random_numbers(1, 100, 10, seed=7)),
            list(random_numbers(1, 100, 10, seed=7)),
        )

    def test_instances_have_independent_state(self) -> None:
        first = random_numbers(1, 100, 5, seed=7)
        second = random_numbers(1, 100, 5, seed=7)
        self.assertEqual(next(first), next(second))
        self.assertEqual(list(first), list(second))

    def test_global_random_state_is_unchanged(self) -> None:
        before = random.getstate()
        list(random_numbers(1, 10, 5, seed=42))
        self.assertEqual(random.getstate(), before)

    def test_stream_can_be_consumed_partially(self) -> None:
        numbers = random_numbers(1, 10, 1_000_000, seed=1)
        self.assertIsInstance(numbers, GeneratorType)
        self.assertEqual(len(list(islice(numbers, 3))), 3)

    def test_invalid_range_and_count(self) -> None:
        for lower, upper, count in ((4, 3, 1), (1, 3, -1)):
            with self.subTest(lower=lower, upper=upper, count=count):
                with self.assertRaises(ValueError):
                    next(random_numbers(lower, upper, count))

    def test_invalid_argument_types(self) -> None:
        arguments = (
            (True, 5, 2), (1, False, 2), (1, 5, True),
            (1.5, 5, 2), (1, 5.0, 2), (1, 5, "2"),
        )
        for lower, upper, count in arguments:
            with self.subTest(lower=lower, upper=upper, count=count):
                with self.assertRaises(TypeError):
                    next(random_numbers(lower, upper, count))
        for seed in (True, 1.5, "7"):
            with self.subTest(seed=seed):
                with self.assertRaises(TypeError):
                    next(random_numbers(1, 5, 2, seed=seed))


if __name__ == "__main__":
    unittest.main()
