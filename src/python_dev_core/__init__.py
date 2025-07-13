"""
python_dev_core
===============

Core utility package for Python development.

Main features:
- Automatic logging functionality
- General-purpose helper functions
- Development support tools
"""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "Hashimoto"
__license__ = "MIT"

# Export logging functionality
from python_dev_core.utils.logging import AutoLogMeta, instrument

__all__ = [
    "AutoLogMeta",
    "__author__",
    "__license__",
    "__version__",
    "instrument",
]
