# python-dev-core

Core utility package for Python development

## Overview

`python-dev-core` is a core package that provides common functionality for Python development. It offers tools to improve development efficiency such as automatic logging capabilities and utility functions.

## Features

- **Automatic Logging**: Automatic log instrumentation using metaclasses and decorators
- **Development Efficiency**: General-purpose helper functions and utilities
- **Type Safety**: Utilizing the latest type hint features from Python 3.13 onwards
- **High-Quality Code**: Quality assurance through strict linting and testing

## Installation

### Installing with pip

```bash
pip install python-dev-core
```

### Development Environment Setup

```bash
git clone https://github.com/yourusername/python-dev-core.git
cd python-dev-core
uv sync
```

## Usage

### Automatic Logging

#### Automatic Class Instrumentation

```python
from python_dev_core import AutoLogMeta

class MyService(metaclass=AutoLogMeta):
    def process_data(self, data: list[str]) -> dict[str, int]:
        # Method start/end is automatically logged
        result = {}
        for item in data:
            result[item] = len(item)
        return result

# Usage example
service = MyService()
service.process_data(["hello", "world"])
# DEBUG: MyService.process_data called with args=(['hello', 'world'],), kwargs={}
# DEBUG: MyService.process_data returned {'hello': 5, 'world': 5} (0.0001 s)
```

#### Module/Function Automatic Instrumentation

```python
from python_dev_core import instrument
import my_module

# Instrument the entire module
instrument(my_module)

# Instrument individual functions
@instrument
def calculate_sum(numbers: list[int]) -> int:
    return sum(numbers)
```

### Controlling Log Level

You can control the log level using the `LOG_LEVEL` environment variable.

```bash
export LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
python your_script.py
```

## Development

### Requirements

- Python 3.13 or higher
- uv (package manager)

### Development Commands

```bash
# Code formatting
make format

# Linting
make lint

# Type checking
make typecheck

# Run tests
make test

# Run all checks
make check
```

## Project Structure

```
python-dev-core/
├── src/
│   └── python_dev_core/
│       ├── __init__.py
│       ├── core/           # Core logic
│       └── utils/          # Utilities
│           ├── __init__.py
│           ├── helpers.py
│           └── logging/    # Logging functionality
├── tests/                  # Test code
├── pyproject.toml         # Project configuration
├── Makefile              # Development tasks
└── README.md             # This file
```

## License

MIT License

## Author

Hashimoto

## Contributing

Bug reports and feature requests are accepted via GitHub issues.

When submitting a pull request:
- Run `make format`, `make lint`, `make typecheck` and ensure all checks pass
- Add tests for new features
- Update documentation