"""Повышенное задание №3: каррирование функции."""

from collections.abc import Callable
from functools import wraps
from inspect import Parameter, signature
from typing import Any, TypeVar

Result = TypeVar("Result")


def curry(function: Callable[..., Result]) -> Callable[..., Any]:
    """Накопить аргументы функции с фиксированной сигнатурой по шагам.

    Функция вызывается, когда заданы все обязательные параметры.
    Поддерживаются позиционные и именованные аргументы и значения
    по умолчанию. *args и **kwargs не поддерживаются: у них нет
    однозначного момента завершения накопления.
    """
    if not callable(function):
        raise TypeError("Для каррирования требуется вызываемый объект")
    parameters = signature(function)
    if any(
        parameter.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD)
        for parameter in parameters.parameters.values()
    ):
        raise ValueError("Нужна функция без *args и **kwargs")

    def build(
        saved_args: tuple[object, ...], saved_kwargs: dict[str, object]
    ) -> Callable[..., Any]:
        """Создать независимый шаг с сохранёнными аргументами."""
        @wraps(function)
        def curried(*args: object, **kwargs: object) -> Any:
            """Принять следующую группу аргументов."""
            repeated = saved_kwargs.keys() & kwargs.keys()
            if repeated:
                raise TypeError("Именованный аргумент уже был передан")
            combined_args = saved_args + args
            combined_kwargs = {**saved_kwargs, **kwargs}
            parameters.bind_partial(*combined_args, **combined_kwargs)
            try:
                parameters.bind(*combined_args, **combined_kwargs)
            except TypeError:
                if not args and not kwargs:
                    raise TypeError("На этом шаге требуется аргумент") from None
                return build(combined_args, combined_kwargs)
            return function(*combined_args, **combined_kwargs)

        return curried

    return build((), {})
