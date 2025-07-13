"""
python_dev_core.utils.logging
==========
* Initialize root logger and perform automatic instrumentation.
"""

from __future__ import annotations

from ._auto_logger import AutoLogMeta, instrument
from ._logconfig import configure_root_logger

# Configure root logger
configure_root_logger()

__all__ = [
    "AutoLogMeta",
    "instrument",
]
