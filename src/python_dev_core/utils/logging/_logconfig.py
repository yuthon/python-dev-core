"""
python_dev_core.utils.logging._logconfig
--------------------
パッケージ全体で共通利用する logging 設定。
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Final

_DEFAULT_LEVEL: Final[int] = logging.INFO
_ENV_VAR: Final[str] = "LOG_LEVEL"


def _resolve_level() -> int:
    """環境変数からログレベルを取得（未設定なら INFO）。"""
    text = os.getenv(_ENV_VAR, "").upper()
    return getattr(logging, text, _DEFAULT_LEVEL)


def configure_root_logger() -> None:
    """
    ルートロガーを設定。

    ★ パッケージ import 時に必ず呼び出される（mypkg_core/__init__.py で実行）。
    """
    level = _resolve_level()

    # 既にハンドラが付いている場合はユーザが手動設定したとみなし、何もしない。
    root = logging.getLogger()
    if root.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="[{asctime}] {levelname:<7} {name}: {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{",
        )
    )
    root.addHandler(handler)
    root.setLevel(level)
