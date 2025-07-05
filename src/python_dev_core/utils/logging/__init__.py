"""
python_dev_core.utils.logging
==========
* ルートロガー初期化と自動計装を行う。
"""

from __future__ import annotations

from ._auto_logger import AutoLogMeta, instrument
from ._logconfig import configure_root_logger

# ルートロガー設定
configure_root_logger()

__all__ = [
    "AutoLogMeta",
    "instrument",
]
