"""Проверки бесконечного потока случайных записей."""

import random
import unittest
from itertools import islice
from types import GeneratorType

from lab4_tasks.random_data import random_records


class RandomRecordsTests(unittest.TestCase):
    def test_record_schema_and_value_range(self) -> None:
        records = list(islice(random_records(seed=42), 100))
        self.assertEqual([row["id"] for row in records], list(range(1, 101)))
        for row in records:
            self.assertEqual(set(row), {"id", "category", "value"})
            self.assertIn(row["category"], {"A", "B", "C"})
            self.assertIs(type(row["value"]), int)
            self.assertTrue(0 <= row["value"] <= 100)

    def test_same_seed_reproduces_records(self) -> None:
        first = list(islice(random_records(seed=7), 10))
        second = list(islice(random_records(seed=7), 10))
        self.assertEqual(first, second)

    def test_generator_continues_after_first_sample(self) -> None:
        records = random_records(seed=7)
        self.assertIsInstance(records, GeneratorType)
        self.assertEqual(len(list(islice(records, 10_000))), 10_000)
        self.assertEqual(next(records)["id"], 10_001)

    def test_emitted_records_are_independent(self) -> None:
        records = random_records(seed=7)
        first = next(records)
        saved = first.copy()
        second = next(records)
        self.assertIsNot(first, second)
        self.assertEqual(first, saved)
        second["category"] = "Изменено"
        self.assertEqual(first, saved)

    def test_instances_have_independent_state(self) -> None:
        first = random_records(seed=42)
        second = random_records(seed=42)
        self.assertEqual(next(first), next(second))
        self.assertEqual(
            list(islice(first, 5)), list(islice(second, 5))
        )

    def test_global_random_state_is_unchanged(self) -> None:
        before = random.getstate()
        list(islice(random_records(seed=42), 5))
        self.assertEqual(random.getstate(), before)

    def test_invalid_seed(self) -> None:
        for seed in (True, "42", 1.5):
            with self.subTest(seed=seed):
                with self.assertRaises(TypeError):
                    next(random_records(seed=seed))


if __name__ == "__main__":
    unittest.main()
