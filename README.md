<a href="https://www.ultralytics.com/"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

# ⚡️ `autoimport`: Effortless Lazy Imports in Python

`autoimport` is a lightweight Python package providing effortless **lazy imports**. By using the `lazy` context manager, modules are imported only when they are actually accessed, improving application startup times and reducing the initial memory footprint. This is ideal for projects with heavy dependencies that are not always needed immediately. The `ultralytics-autoimport` package is published on [PyPI](https://pypi.org/project/ultralytics-autoimport/) for easy installation.

[![autoimport CI](https://github.com/ultralytics/autoimport/actions/workflows/ci.yml/badge.svg)](https://github.com/ultralytics/autoimport/actions/workflows/ci.yml)
[![Ultralytics Actions](https://github.com/ultralytics/autoimport/actions/workflows/format.yml/badge.svg)](https://github.com/ultralytics/autoimport/actions/workflows/format.yml)
[![Ultralytics Discord](https://img.shields.io/discord/1089800235347353640?logo=discord&logoColor=white&label=Discord&color=blue)](https://discord.com/invite/ultralytics)
[![Ultralytics Forums](https://img.shields.io/discourse/users?server=https%3A%2F%2Fcommunity.ultralytics.com&logo=discourse&label=Forums&color=blue)](https://community.ultralytics.com/)
[![Ultralytics Reddit](https://img.shields.io/reddit/subreddit-subscribers/ultralytics?style=flat&logo=reddit&logoColor=white&label=Reddit&color=blue)](https://reddit.com/r/ultralytics)

## 🚀 Quick Start

Install the `ultralytics-autoimport` package from [PyPI](https://pypi.org/project/ultralytics-autoimport/):

[![PyPI - Version](https://img.shields.io/pypi/v/ultralytics-autoimport.svg)](https://pypi.org/project/ultralytics-autoimport/)
[![Downloads](https://static.pepy.tech/badge/ultralytics-autoimport)](https://clickpy.clickhouse.com/dashboard/ultralytics-autoimport)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ultralytics-autoimport.svg)](https://pypi.org/project/ultralytics-autoimport/)

```bash
pip install ultralytics-autoimport
```

Use the `lazy` context manager to defer imports according to standard [Python import mechanics](https://docs.python.org/3/reference/import.html):

```python
import time

from autoimport import lazy

with lazy():
    t0 = time.perf_counter()
    import torch  # Import is deferred until first use

    print(f"Initial import time: {time.perf_counter() - t0:.3f}s")  # Example output: 0.000s

t1 = time.perf_counter()
# The package is actually loaded here when torch.cuda is accessed
torch.cuda.is_available()
print(f"First use time: {time.perf_counter() - t1:.3f}s")  # Example output: 0.462s
```

In this example, the `import torch` statement inside the `lazy()` context doesn't immediately load the [PyTorch](https://pytorch.org/) library. The actual import happens only when `torch.cuda.is_available()` is called, demonstrating the deferred loading mechanism.

## 🗂 Repository Structure

The repository is organized for clarity and ease of development:

- `autoimport/`: Contains the source code of the `autoimport` package.
- `tests/`: Unit tests to ensure code reliability using frameworks like [pytest](https://docs.pytest.org/en/stable/).
- `pyproject.toml`: Project configuration following [PEP 621](https://peps.python.org/pep-0621/), including dependencies and packaging details.
- `.gitignore`: Specifies files intentionally untracked by Git.
- `LICENSE`: The open-source license for the project ([AGPL-3.0](https://opensource.org/license/agpl-v3)).
- `.github/workflows/`: [GitHub Actions](https://docs.github.com/en/actions) workflows for Continuous Integration (CI) and Continuous Deployment (CD).

```
autoimport/
│
├── autoimport/           # Package source code
│   ├── __init__.py
│   └── ...
│
├── tests/                # Unit tests
│   ├── __init__.py
│   ├── test_autoimport.py
│   └── ...
│
├── pyproject.toml        # Project configuration
├── .gitignore            # Git ignore rules
├── LICENSE               # AGPL-3.0 License file
├── README.md             # This file
└── .github/workflows/    # GitHub Actions CI/CD workflows
    ├── ci.yml
    └── format.yml
```

### 📂 Source Code in `autoimport/` Directory

The `autoimport/` directory contains the core Python code for the `autoimport` package.

### 🧪 Testing with the `tests/` Directory

The `tests/` directory includes tests designed to maintain code quality and prevent regressions during development.

## ➕ Starting a New Project

This repository can also serve as a template for new Python projects at [Ultralytics](https://www.ultralytics.com/).

To use it as a template:

1.  **Create a New Repository:** Use this repository as a template to generate a new one for your project.
2.  **Customize:** Modify `pyproject.toml`, `.pre-commit-config.yaml` (if using [pre-commit](https://pre-commit.com/)), and GitHub workflow YAML files as needed for your specific project requirements.
3.  **Develop:** Add your source code to a new directory (e.g., `your_package_name/`) and corresponding tests to the `tests/` directory.
4.  **Document:** Update the README.md file and add any necessary documentation within the [Ultralytics Docs](https://docs.ultralytics.com/).
5.  **CI/CD:** Utilize the pre-configured [GitHub Actions](https://docs.github.com/en/actions) for automated testing and formatting checks.

## 💡 Contribute

Ultralytics thrives on community contributions! We appreciate any help, from reporting bugs to submitting pull requests. Please see our [Contributing Guide](https://docs.ultralytics.com/help/contributing/) for more details on how to get involved. You can also share your feedback through our quick [Survey](https://www.ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey). Thank you 🙏 to all our contributors!

[![Ultralytics open-source contributors](https://raw.githubusercontent.com/ultralytics/assets/main/im/image-contributors.png)](https://github.com/ultralytics/autoimport/graphs/contributors)

## 📄 License

Ultralytics provides two licensing options to accommodate different use cases:

- **AGPL-3.0 License**: This [OSI-approved](https://opensource.org/license) open-source license is ideal for students, enthusiasts, and researchers who wish to share their work openly. See the [LICENSE](https://github.com/ultralytics/autoimport/blob/main/LICENSE) file for full details.
- **Enterprise License**: Designed for commercial use, this license allows for the integration of Ultralytics software and AI models into commercial products and services without the open-source requirements of AGPL-3.0. Please contact [Ultralytics Licensing](https://www.ultralytics.com/license) for more information.

## 📮 Contact

For bug reports, feature requests, or questions, please open a [GitHub Issue](https://github.com/ultralytics/autoimport/issues). For community support and discussions, join our [Discord](https://discord.com/invite/ultralytics) server!

<br>
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="3%" alt="Ultralytics GitHub"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="3%" alt="Ultralytics LinkedIn"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://twitter.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="3%" alt="Ultralytics Twitter"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://youtube.com/ultralytics?sub_confirmation=1"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="3%" alt="Ultralytics YouTube"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="3%" alt="Ultralytics TikTok"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://ultralytics.com/bilibili"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-bilibili.png" width="3%" alt="Ultralytics BiliBili"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://discord.com/invite/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>
