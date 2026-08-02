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

## 📦 Installation

```bash
pip install ultralytics-autoimport
```

## 💻 Usage

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

## ⚠️ Scope and Limitations

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

First execution of lazy module bodies is serialized process-wide. This prevents two lazy modules from deadlocking each
other during concurrent circular initialization, but it also means unrelated first accesses cannot initialize in
parallel. Module bodies run while that shared reentrant lock is held, so applications should avoid coordinating lazy
first access with other threads during import-time synchronization.

The discovered loader must support `exec_module()`, and its module object must permit `__class__` reassignment. These are
the same compatibility requirements as Python's `importlib.util.LazyLoader`; incompatible custom loaders fail during
`lazy_import()` instead of returning a partial proxy.

Versions before 0.1.0 exposed a `with lazy():` context manager that replaced `builtins.__import__`. That design could not
preserve normal Python behavior for aliases, function-local imports, dotted imports, or objects imported with
`from ... import ...`, and it affected imports in every thread. Replace it with explicit module assignments.

## 🐍 Python 3.15 and PEP 810

Python 3.15 adds native lazy imports through accepted
[PEP 810](https://peps.python.org/pep-0810/). Its interpreter-supported syntax can lazily bind both modules and imported
attributes:

```python
lazy from pathlib import Path

lazy import torch
```

PEP 810 also provides a migration form that keeps ordinary import statements:

```pycon
>>> __lazy_modules__ = {"numpy", "torch"}
>>> import numpy as np
>>> import torch
```

On Python 3.15, the listed imports are lazy. Earlier Python versions ignore `__lazy_modules__` and import them eagerly,
which lets libraries adopt the declaration before dropping older versions. Native lazy imports are the preferred
long-term solution because the interpreter can replace a lazy binding with any real module, class, function, or constant
before Python code uses it. `autoimport` remains a narrow module-only option for Python 3.8 through 3.14.

## 🛠️ Development

```bash
uv pip install -e .
python -m unittest discover tests -v
ruff format .
ruff check .
```

## 💡 Contribute

Ultralytics thrives on community collaboration, and we deeply value your contributions! Whether it's reporting bugs, suggesting features, or submitting code changes, your involvement is crucial.

- **Reporting Issues**: Encounter a bug? Please report it on [GitHub Issues](https://github.com/ultralytics/autoimport/issues).
- **Feature Requests**: Have an idea for improvement? Share it via [GitHub Issues](https://github.com/ultralytics/autoimport/issues).
- **Pull Requests**: Want to contribute code? Please read our [Contributing Guide](https://docs.ultralytics.com/help/contributing) first, then submit a Pull Request.
- **Feedback**: Share your thoughts and experiences by participating in our official [Survey](https://www.ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey).

A heartfelt thank you 🙏 goes out to all our contributors! Your efforts help make Ultralytics tools better for everyone.

[![Ultralytics open-source contributors](https://raw.githubusercontent.com/ultralytics/assets/main/im/image-contributors.png)](https://github.com/ultralytics/ultralytics/graphs/contributors)

## 📄 License

Ultralytics offers two licensing options to accommodate diverse needs:

- **AGPL-3.0 License**: Ideal for students, researchers, and enthusiasts passionate about open collaboration and knowledge sharing. This [OSI-approved](https://opensource.org/license/agpl-3.0) open-source license promotes transparency and community involvement. See the [LICENSE](LICENSE) file for details.
- **Enterprise License**: Designed for commercial applications, this license permits the seamless integration of Ultralytics software and AI models into commercial products and services, bypassing the copyleft requirements of AGPL-3.0. For commercial use cases, please inquire about an [Ultralytics Enterprise License](https://www.ultralytics.com/license).

## 📮 Contact

For bug reports or feature suggestions, please use [GitHub Issues](https://github.com/ultralytics/autoimport/issues). For general questions, discussions, and community support, join our [Discord](https://discord.com/invite/ultralytics) server!

<br>
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="3%" alt="Ultralytics GitHub"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="3%" alt="Ultralytics LinkedIn"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://twitter.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="3%" alt="Ultralytics Twitter"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.youtube.com/ultralytics?sub_confirmation=1"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="3%" alt="Ultralytics YouTube"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="3%" alt="Ultralytics TikTok"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://ultralytics.com/bilibili"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-bilibili.png" width="3%" alt="Ultralytics BiliBili"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://discord.com/invite/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>
