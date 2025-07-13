"""
python_dev_core.utils.logging._auto_logger
----------------------
Decorator and metaclass for DEBUG logging of function/method start and end.
"""

from __future__ import annotations

import functools
import inspect
import logging
from collections.abc import Callable
from time import perf_counter
from types import FunctionType
from typing import Any, cast


def _log_call[F: Callable[..., Any]](fn: F) -> F:
    """
    Decorator to instrument a single function/method.

    * On call:
        DEBUG "[func] ⇢ args=%s, kwargs=%s"
    * On normal exit:
        DEBUG "[func] ⇠ return=%s (%.4f s)"
    * On exception:
        DEBUG "[func] !! raised"
        → Exception propagates as-is
    """
    logger = logging.getLogger(fn.__module__)

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("%s ⇢ args=%s, kwargs=%s", fn.__qualname__, args, kwargs)

        start = perf_counter()
        try:
            result = fn(*args, **kwargs)
        except Exception:
            if logger.isEnabledFor(logging.DEBUG):
                logger.exception("%s !! raised", fn.__qualname__)
            raise
        if logger.isEnabledFor(logging.DEBUG):
            dur = perf_counter() - start
            logger.debug("%s ⇠ return=%s (%.4f s)", fn.__qualname__, result, dur)
        return result

    return cast(F, wrapper)


def _should_wrap(obj: Any) -> bool:
    """Should this object be wrapped?"""
    return isinstance(obj, FunctionType) and not obj.__name__.startswith("_")


def instrument(obj: Any) -> Any:
    """
    * Takes a module, function, or class and recursively wraps
      non-private elements with _log_call
    * Marks with "__instrumented__" attribute to prevent duplicate wrapping
    """
    if getattr(obj, "__instrumented__", False):
        return obj

    if inspect.ismodule(obj):
        for name, member in inspect.getmembers(obj):
            if _should_wrap(member):
                setattr(obj, name, _log_call(member))
            elif inspect.isclass(member):
                instrument(member)

    elif inspect.isclass(obj):
        for name, member in inspect.getmembers(obj):
            if _should_wrap(member):
                setattr(obj, name, _log_call(member))

        # To instrument dynamic attribute access,
        # additional implementation like replacing __getattribute__ is possible.

    elif callable(obj):  # function
        obj = _log_call(obj)

    obj.__instrumented__ = True
    return obj


class AutoLogMeta(type):
    """
    Metaclass with automatic instrumentation.

    When declaring `class Foo(metaclass=AutoLogMeta): ...`,
    all public methods are instrumented.
    """

    def __new__(
        mcls: type[AutoLogMeta],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> type:
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        return cast(type, instrument(cls))
