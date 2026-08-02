<a href="https://www.ultralytics.com/"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

# ⚡️ `autoimport`: Explicit Lazy Module Imports

`autoimport` defers execution of a Python module until its first attribute access. It builds on Python's standard
[`importlib` loader protocol](https://docs.python.org/3/library/importlib.html), preserving the canonical module object
and its identity in `sys.modules`.

The `ultralytics-autoimport` package supports Python 3.8 through 3.14.

[![autoimport CI](https://github.com/ultralytics/autoimport/actions/workflows/ci.yml/badge.svg)](https://github.com/ultralytics/autoimport/actions/workflows/ci.yml)
[![Ultralytics Actions](https://github.com/ultralytics/autoimport/actions/workflows/format.yml/badge.svg)](https://github.com/ultralytics/autoimport/actions/workflows/format.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/ultralytics-autoimport.svg)](https://pypi.org/project/ultralytics-autoimport/)
[![Downloads](https://static.pepy.tech/badge/ultralytics-autoimport)](https://clickpy.clickhouse.com/dashboard/ultralytics-autoimport)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ultralytics-autoimport.svg)](https://pypi.org/project/ultralytics-autoimport/)

## Installation

```bash
pip install ultralytics-autoimport
```

## Usage

Replace a module import with an explicit lazy assignment:

```python
import time

from autoimport import lazy_import

t0 = time.perf_counter()
torch = lazy_import("torch")  # Finds torch now, but does not execute torch/__init__.py yet
print(f"Setup: {time.perf_counter() - t0:.3f}s")

t1 = time.perf_counter()
torch.cuda.is_available()  # First attribute access executes and initializes torch
print(f"First use: {time.perf_counter() - t1:.3f}s")

torch.tensor([1, 2, 3])  # Later attributes use the fully initialized module normally
```

Aliases and dotted modules are explicit strings:

```python
np = lazy_import("numpy")
linalg = lazy_import("numpy.linalg")
```

If the requested module is already imported, `lazy_import()` returns the existing object unchanged. Module discovery
happens immediately, so a misspelled or unavailable module raises `ModuleNotFoundError` at the `lazy_import()` call.
For dotted names, Python may import parent packages while finding the requested child module.

## Scope and Limitations

`lazy_import()` deliberately supports modules only. It does not emulate arbitrary `from ... import ...` bindings:

```python
# Supported
pathlib = lazy_import("pathlib")
path = pathlib.Path("models")

# Not provided: transparent lazy classes, functions, or constants
# Path = lazy_import("pathlib.Path")
```

Deferring a module also defers its import-time side effects and any exception raised while executing its body. Those
effects or errors occur on first attribute access instead of at the assignment. If code immediately accesses the module
after `lazy_import()`, there is no startup benefit.

The discovered loader must support `exec_module()`, and its module object must permit `__class__` reassignment. These are
the same compatibility requirements as Python's `importlib.util.LazyLoader`; incompatible custom loaders fail during
`lazy_import()` instead of returning a partial proxy.

Versions before 0.1.0 exposed a `with lazy():` context manager that replaced `builtins.__import__`. That design could not
preserve normal Python behavior for aliases, function-local imports, dotted imports, or objects imported with
`from ... import ...`, and it affected imports in every thread. Replace it with explicit module assignments.

## Python 3.15 and PEP 810

Python 3.15 adds native lazy imports through accepted
[PEP 810](https://peps.python.org/pep-0810/). Its interpreter-supported syntax can lazily bind both modules and imported
attributes:

```python
lazy from pathlib import Path

lazy import torch
```

PEP 810 also provides a migration form that keeps ordinary import statements:

```python
__lazy_modules__ = {"numpy", "torch"}
```

On Python 3.15, the listed imports are lazy. Earlier Python versions ignore `__lazy_modules__` and import them eagerly,
which lets libraries adopt the declaration before dropping older versions. Native lazy imports are the preferred
long-term solution because the interpreter can replace a lazy binding with any real module, class, function, or constant
before Python code uses it. `autoimport` remains a narrow module-only option for Python 3.8 through 3.14.

## Development

```bash
uv pip install -e .
python -m unittest discover tests -v
ruff format .
ruff check .
```

## License

Ultralytics offers AGPL-3.0 and Enterprise licenses. See [LICENSE](LICENSE) and the
[Ultralytics licensing page](https://www.ultralytics.com/license).

For bug reports and feature requests, open a [GitHub issue](https://github.com/ultralytics/autoimport/issues).
