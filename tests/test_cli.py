"""Проверки реального запуска CLI из другого каталога."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


class CommandLineTests(unittest.TestCase):
    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        """Запустить main.py отдельным процессом во временном каталоге."""
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        with tempfile.TemporaryDirectory() as directory:
            return subprocess.run(
                [sys.executable, "-B", str(PROJECT / "main.py"), *arguments],
                cwd=directory,
                env=environment,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=15,
            )

    def test_commands_from_another_directory(self) -> None:
        examples = (
            (("sum", "1", "2", "3"), "6\n"),
            (("fibonacci", "7"), "0 1 1 2 3 5 8\n"),
            (("random", "3", "3", "4"), "3 3 3 3\n"),
            (("curry", "2", "3", "4"), "24\n"),
        )
        for arguments, expected in examples:
            with self.subTest(arguments=arguments):
                result = self.run_cli(*arguments)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, expected)
                self.assertEqual(result.stderr, "")

    def test_fractional_numbers_keep_their_value(self) -> None:
        result = self.run_cli("sum", "1", "2.5", "-0.25")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "3.25\n")

    def test_empty_sum(self) -> None:
        result = self.run_cli("sum")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "0\n")

    def test_records_command_produces_json_lines(self) -> None:
        result = self.run_cli("records", "3", "--seed", "42")
        self.assertEqual(result.returncode, 0, result.stderr)
        records = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual([record["id"] for record in records], [1, 2, 3])
        self.assertEqual(result.stderr, "")

    def test_zero_count(self) -> None:
        for arguments in (
            ("fibonacci", "0"), ("random", "1", "10", "0"),
            ("records", "0"),
        ):
            with self.subTest(arguments=arguments):
                result = self.run_cli(*arguments)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), "")

    def test_invalid_arguments_are_rejected(self) -> None:
        examples = (
            ("fibonacci", "-1"), ("records", "-1"),
            ("random", "0", "5", "-1"), ("records", "1.5"),
            ("sum", "nan"), ("sum", "True"),
            ("curry", "2", "inf", "3"),
            ("records", "2", "--seed", "True"),
        )
        for arguments in examples:
            with self.subTest(arguments=arguments):
                result = self.run_cli(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertNotEqual(result.stderr, "")
                self.assertEqual(result.stdout, "")

    def test_invalid_range_is_reported_to_stderr(self) -> None:
        result = self.run_cli("random", "5", "1", "2")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("Ошибка:", result.stderr)

    def test_seed_option_reproduces_output(self) -> None:
        for arguments in (
            ("random", "1", "100", "8", "--seed", "7"),
            ("records", "3", "--seed", "7"),
        ):
            with self.subTest(arguments=arguments):
                first = self.run_cli(*arguments)
                second = self.run_cli(*arguments)
                self.assertEqual(first.returncode, 0, first.stderr)
                self.assertEqual(second.returncode, 0, second.stderr)
                self.assertEqual(first.stdout, second.stdout)

    def test_all_demonstrations_finish(self) -> None:
        result = self.run_cli("all")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        for task in ("sum", "fibonacci", "random", "curry", "records"):
            self.assertIn(f"--- {task} ---", result.stdout)

    def test_missing_or_unknown_command(self) -> None:
        for arguments in ((), ("unknown",)):
            with self.subTest(arguments=arguments):
                result = self.run_cli(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertNotEqual(result.stderr, "")

    def test_module_entry_point(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", "-m", "lab4_tasks", "sum", "2", "3"],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "5\n")


if __name__ == "__main__":
    unittest.main()
