"""
python_dev_core
===============

Python開発のためのコアユーティリティパッケージ。

主な機能:
- 自動ロギング機能
- 汎用ヘルパー関数
- 開発支援ツール
"""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "Hashimoto"
__license__ = "MIT"

# ロギング機能のエクスポート
from python_dev_core.utils.logging import AutoLogMeta, instrument

__all__ = [
    "AutoLogMeta",
    "__author__",
    "__license__",
    "__version__",
    "instrument",
]
