<a href="https://www.ultralytics.com/" target="_blank"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

# ⚡️ `autoimport`: Effortless Lazy Imports in Python

`autoimport` is a lightweight Python package that provides effortless lazy imports. By using the `lazy` context manager, modules are imported only when they are actually accessed, improving startup times and reducing initial memory footprint. Ideal for projects with heavy dependencies that are not always needed. The `ultralytics-autoimport` package is published on PyPI for easy installation.

[![autoimport CI](https://github.com/ultralytics/autoimport/actions/workflows/ci.yml/badge.svg)](https://github.com/ultralytics/autoimport/actions/workflows/ci.yml) [![Ultralytics Actions](https://github.com/ultralytics/autoimport/actions/workflows/format.yml/badge.svg)](https://github.com/ultralytics/autoimport/actions/workflows/format.yml) <a href="https://discord.com/invite/ultralytics"><img alt="Discord" src="https://img.shields.io/discord/1089800235347353640?logo=discord&logoColor=white&label=Discord&color=blue"></a> <a href="https://community.ultralytics.com/"><img alt="Ultralytics Forums" src="https://img.shields.io/discourse/users?server=https%3A%2F%2Fcommunity.ultralytics.com&logo=discourse&label=Forums&color=blue"></a> <a href="https://reddit.com/r/ultralytics"><img alt="Ultralytics Reddit" src="https://img.shields.io/reddit/subreddit-subscribers/ultralytics?style=flat&logo=reddit&logoColor=white&label=Reddit&color=blue"></a>

## 🚀 Quick Start

Install the `ultralytics-autoimport` package from PyPI:

[![PyPI - Version](https://img.shields.io/pypi/v/ultralytics-autoimport.svg)](https://pypi.org/project/ultralytics-autoimport/)
[![Downloads](https://static.pepy.tech/badge/ultralytics-autoimport)](https://www.pepy.tech/projects/ultralytics-autoimport)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ultralytics-autoimport.svg)](https://pypi.org/project/ultralytics-autoimport/)

```bash
pip install ultralytics-autoimport
```

Use the `lazy` context manager to defer imports:

```python
from autoimport import lazy

with lazy():
    import torch  # torch is only imported when used

    print("Torch imported:", "torch" in globals())
    torch.cuda.is_available()  # Now torch is imported
    print("Torch imported:", "torch" in globals())
```

## 🗂 Repository Structure

The repository is organized for clarity and ease of development:

- `autoimport/`: Contains the source code of the `autoimport` package.
- `tests/`: Unit tests to ensure code reliability.
- `pyproject.toml`: Project configuration, including dependencies and packaging details.
- `.gitignore`: Specifies files to be excluded from Git tracking.
- `LICENSE`: The open-source license for the project (AGPL-3.0).
- `.github/workflows/`: GitHub Actions workflows for CI/CD.

```
autoimport/
│
├── autoimport/
│   ├── __init__.py
│   └── ...
│
├── tests/
│   ├── __init__.py
│   ├── test_autoimport.py
│   └── ...
│
├── pyproject.toml
└── README.md
```

### Source Code in `src/autoimport/` Directory 📂

The `src/autoimport/` directory contains the core Python code for the `autoimport` package.

### Testing with the `tests/` Directory 🧪

The `tests/` directory includes tests to maintain code quality and prevent regressions.

## ➕ Starting a New Project

This repository can also serve as a template for new Python projects at [Ultralytics](https://www.ultralytics.com/).

To use it as a template:

1. **Create a New Repository:** Use this as a template to generate a new repository.
2. **Customize:** Modify `pyproject.toml`, `.pre-commit-config.yaml` (if applicable), and GitHub workflow YAMLs as needed.
3. **Develop:** Add your code to `src/your_package_name/` and tests to `tests/`.
4. **Document:** Update the README and add documentation if necessary.
5. **CI/CD:** Utilize the pre-configured GitHub Actions for automated testing.

## 💡 Contribute

Ultralytics thrives on community contributions! Please see our [Contributing Guide](https://docs.ultralytics.com/help/contributing/) for details on how to participate. Share your feedback in our [Survey](https://www.ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey). Thank you 🙏 to all our contributors!

<a href="https://github.com/ultralytics/yolov5/graphs/contributors">
<img width="100%" src="https://github.com/ultralytics/assets/raw/main/im/image-contributors.png" alt="Ultralytics open-source contributors"></a>

## 📄 License

Ultralytics offers two licensing options:

- **AGPL-3.0 License**: An OSI-approved open-source license for students, enthusiasts, and researchers. See [LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) for details.
- **Enterprise License**: For commercial use, allowing integration of Ultralytics software and AI models into commercial products without the AGPL-3.0 copyleft restrictions. Contact [Ultralytics Licensing](https://www.ultralytics.com/license) if this is required.

## 📮 Contact

For issues or feature suggestions, please open a [GitHub Issue](https://github.com/ultralytics/autoimport/issues). You can also join our [Discord](https://discord.com/invite/ultralytics) community!

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
