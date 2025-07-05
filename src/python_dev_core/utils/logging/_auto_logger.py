"""
python_dev_core.utils.logging._auto_logger
----------------------
関数・メソッドの開始／終了を DEBUG ログするデコレータとメタクラス。
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
    単一の関数 / メソッドを計装するデコレータ。

    * 呼び出し時：
        DEBUG "[func] ⇢ args=%s, kwargs=%s"
    * 正常終了：
        DEBUG "[func] ⇠ return=%s (%.4f s)"
    * 例外発生：
        DEBUG "[func] !! raised"
        → 例外はそのまま伝播
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
    """wrap 対象か？"""
    return isinstance(obj, FunctionType) and not obj.__name__.startswith("_")


def instrument(obj: Any) -> Any:
    """
    * モジュール、関数、クラスのいずれかを受け取り、
      非 private 要素を再帰的に _log_call で包む
    * 重複包み込み防止のため「__instrumented__」属性でマーク
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

        # 動的属性アクセスも対象にしたい場合、
        # __getattribute__ を差し替えるなど追加実装可。

    elif callable(obj):  # 関数
        obj = _log_call(obj)

    obj.__instrumented__ = True
    return obj


class AutoLogMeta(type):
    """
    自動計装付きメタクラス。

    `class Foo(metaclass=AutoLogMeta): ...` と宣言すると
    public メソッドは全て計装される。
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
