"""Проверки свёртки последовательностей через reduce."""

import unittest

from lab4_tasks.reduction import sum_with_reduce


class ReductionTests(unittest.TestCase):
    def test_empty_input_has_zero_sum(self) -> None:
        self.assertEqual(sum_with_reduce([]), 0)

    def test_integer_sum_and_negative_values(self) -> None:
        result = sum_with_reduce([10, -3, 0, 5])
        self.assertEqual(result, 12)
        self.assertIsInstance(result, int)

    def test_float_sum(self) -> None:
        self.assertAlmostEqual(sum_with_reduce([1, 2.5, -0.25]), 3.25)

    def test_one_pass_iterator(self) -> None:
        numbers = (number for number in range(5))
        self.assertEqual(sum_with_reduce(numbers), 10)
        self.assertEqual(list(numbers), [])

    def test_large_integers_remain_exact(self) -> None:
        self.assertEqual(sum_with_reduce([10 ** 100, 1]), 10 ** 100 + 1)

    def test_invalid_elements_are_rejected(self) -> None:
        for value in (True, "3", None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    sum_with_reduce([1, value])
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    sum_with_reduce([value])

    def test_non_finite_float_result_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            sum_with_reduce([1e308, 1e308])


if __name__ == "__main__":
    unittest.main()
