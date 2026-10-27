"""Проверки накопления аргументов и независимых замыканий."""

import unittest

from lab4_tasks.currying import curry


def multiply(a: int, b: int, c: int) -> int:
    """Перемножить три числа."""
    return a * b * c


class CurryingTests(unittest.TestCase):
    def test_one_argument_per_step(self) -> None:
        self.assertEqual(curry(multiply)(2)(3)(4), 24)

    def test_argument_groups(self) -> None:
        function = curry(multiply)
        self.assertEqual(function(2, 3)(4), 24)
        self.assertEqual(function(2)(3, 4), 24)
        self.assertEqual(function(2, 3, 4), 24)

    def test_keyword_arguments(self) -> None:
        function = curry(multiply)
        self.assertEqual(function(c=4)(a=2)(b=3), 24)
        self.assertEqual(function(2)(b=3, c=4), 24)

    def test_partial_functions_can_be_reused(self) -> None:
        times_two = curry(multiply)(2)
        self.assertEqual(times_two(3)(4), 24)
        self.assertEqual(times_two(5)(6), 60)
        self.assertEqual(times_two(3)(4), 24)

    def test_function_metadata_is_preserved(self) -> None:
        function = curry(multiply)
        self.assertEqual(function.__name__, "multiply")
        self.assertEqual(function.__doc__, multiply.__doc__)
        self.assertIs(function.__wrapped__, multiply)

    def test_default_parameter(self) -> None:
        def power(base: int, exponent: int = 2) -> int:
            """Возвести число в степень."""
            return base ** exponent

        self.assertEqual(curry(power)(3), 9)
        self.assertEqual(curry(power)(exponent=3)(base=2), 8)

    def test_positional_only_and_keyword_only_parameters(self) -> None:
        def difference(a: int, /, *, b: int) -> int:
            """Вычесть именованный аргумент из позиционного."""
            return a - b

        self.assertEqual(curry(difference)(5)(b=2), 3)
        with self.assertRaises(TypeError):
            curry(difference)(a=5)

    def test_no_argument_function(self) -> None:
        self.assertEqual(curry(lambda: 7)(), 7)

    def test_incorrect_arguments_fail_at_current_step(self) -> None:
        function = curry(multiply)
        with self.assertRaises(TypeError):
            function(1, 2, 3, 4)
        with self.assertRaises(TypeError):
            function(unknown=1)
        with self.assertRaises(TypeError):
            function(a=1)(a=2)
        with self.assertRaises(TypeError):
            function(1)(a=2)
        with self.assertRaises(TypeError):
            function()

    def test_non_callable_and_variadic_functions_are_rejected(self) -> None:
        with self.assertRaises(TypeError):
            curry(123)
        with self.assertRaises(ValueError):
            curry(lambda *args: args)
        with self.assertRaises(ValueError):
            curry(lambda **kwargs: kwargs)

    def test_exception_from_original_function_is_not_swallowed(self) -> None:
        def fail(a: int, b: int) -> int:
            """Имитировать ошибку внутри исходной функции."""
            raise TypeError("Ошибка исходной функции")

        with self.assertRaisesRegex(TypeError, "Ошибка исходной функции"):
            curry(fail)(1)(2)


if __name__ == "__main__":
    unittest.main()
