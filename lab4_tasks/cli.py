"""Командный интерфейс для функциональных заданий."""

import argparse
import json
import sys
from collections.abc import Sequence
from itertools import islice

from .currying import curry
from .demos import show_demos
from .fibonacci import fibonacci_numbers
from .random_data import random_numbers, random_records
from .reduction import sum_with_reduce
from .validation import Number, require_count, require_number


def number_argument(text: str) -> Number:
    """Прочитать int, а при необходимости float, сохраняя тип числа."""
    try:
        number = int(text)
    except ValueError:
        try:
            number = float(text)
        except ValueError as error:
            raise argparse.ArgumentTypeError("Требуется число") from error
    try:
        return require_number(number)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def count_argument(text: str) -> int:
    """Прочитать неотрицательное целое количество элементов."""
    try:
        return require_count(int(text))
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "Количество должно быть неотрицательным целым числом"
        ) from error


def build_parser() -> argparse.ArgumentParser:
    """Описать отдельную команду для каждого задания."""
    parser = argparse.ArgumentParser(description="Лабораторная №4, вариант 3")
    commands = parser.add_subparsers(dest="command", required=True)

    sum_parser = commands.add_parser("sum", help="сумма через reduce")
    sum_parser.add_argument("numbers", nargs="*", type=number_argument)

    fibonacci_parser = commands.add_parser(
        "fibonacci", help="первые числа Фибоначчи"
    )
    fibonacci_parser.add_argument("count", type=count_argument)

    random_parser = commands.add_parser(
        "random", help="случайные целые числа в замкнутом диапазоне"
    )
    random_parser.add_argument("lower", type=int)
    random_parser.add_argument("upper", type=int)
    random_parser.add_argument("count", type=count_argument)
    random_parser.add_argument("--seed", type=int, default=None)

    curry_parser = commands.add_parser(
        "curry", help="каррированное произведение трёх чисел"
    )
    for name in ("a", "b", "c"):
        curry_parser.add_argument(name, type=number_argument)

    records_parser = commands.add_parser(
        "records", help="конечная выборка из бесконечного потока записей"
    )
    records_parser.add_argument("count", type=count_argument)
    records_parser.add_argument("--seed", type=int, default=None)

    commands.add_parser("all", help="все пять демонстраций")
    return parser


def run_command(arguments: argparse.Namespace) -> None:
    """Вывести результат выбранного задания."""
    if arguments.command == "sum":
        print(sum_with_reduce(arguments.numbers))
    elif arguments.command == "fibonacci":
        print(*islice(fibonacci_numbers(), arguments.count))
    elif arguments.command == "random":
        print(*random_numbers(
            arguments.lower, arguments.upper, arguments.count,
            seed=arguments.seed,
        ))
    elif arguments.command == "curry":
        multiply = curry(lambda a, b, c: a * b * c)
        result = multiply(arguments.a)(arguments.b)(arguments.c)
        print(require_number(result))
    elif arguments.command == "records":
        for record in islice(
            random_records(seed=arguments.seed), arguments.count
        ):
            print(json.dumps(record, ensure_ascii=False))
    elif arguments.command == "all":
        show_demos()


def main(argv: Sequence[str] | None = None) -> int:
    """Запустить CLI; ошибки вычислений вывести в stderr."""
    arguments = build_parser().parse_args(argv)
    try:
        run_command(arguments)
    except (TypeError, ValueError, OverflowError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0
