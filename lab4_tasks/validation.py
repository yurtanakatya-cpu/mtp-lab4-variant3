"""Общая проверка чисел, границ и количества элементов."""

from math import isfinite

Number = int | float


def require_number(value: Number) -> Number:
    """Принять конечное int или float, исключив bool."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("Элементы должны быть числами int или float")
    if isinstance(value, float) and not isfinite(value):
        raise ValueError("Числа должны быть конечными")
    return value


def require_integer(value: int, name: str) -> int:
    """Проверить целое число, не принимая логические значения."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name}: требуется целое число")
    return value


def require_count(value: int) -> int:
    """Проверить неотрицательное количество элементов."""
    require_integer(value, "Количество")
    if value < 0:
        raise ValueError("Количество не должно быть отрицательным")
    return value
