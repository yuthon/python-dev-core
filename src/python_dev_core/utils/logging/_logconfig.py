"""
python_dev_core.utils.logging._logconfig
--------------------
Logging configuration shared across the entire package.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Final

_DEFAULT_LEVEL: Final[int] = logging.INFO
_ENV_VAR: Final[str] = "LOG_LEVEL"


def _resolve_level() -> int:
    """Get log level from environment variable (defaults to INFO if not set)."""
    text = os.getenv(_ENV_VAR, "").upper()
    return getattr(logging, text, _DEFAULT_LEVEL)


def configure_root_logger() -> None:
    """
    Configure the root logger.

    ★ Always called when the package is imported (executed in mypkg_core/__init__.py).
    """
    level = _resolve_level()

    # If handlers are already attached, assume user has configured manually
    # and do nothing.
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
