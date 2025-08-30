<a href="https://www.ultralytics.com/"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

# Tests Directory (`tests/`)

Welcome to the `tests/` directory for this Ultralytics project. This directory is crucial for maintaining code quality and reliability through automated testing. We provide support for two popular Python testing frameworks: **pytest** and **unittest**.

## 🧪 Overview

-   **Purpose:** Contains all automated test scripts written in Python to verify the functionality of the project's codebase.
-   **Organization:** The structure mirrors the `src/` directory where possible, making it intuitive to locate tests corresponding to specific modules or features.
-   **Goal:** Ensure comprehensive test coverage, including unit tests, integration tests, and functional tests, covering a wide range of scenarios and edge cases. Good testing practices are fundamental to robust software development, as outlined in resources like [Real Python's guide to testing](https://realpython.com/python-testing/).

## ▶️ Running Tests

You can execute the test suite using either `pytest` or the built-in `unittest` module.

### Option 1: Using `pytest` (Recommended)

[pytest](https://docs.pytest.org/en/stable/) is a mature, feature-rich testing framework for Python that simplifies writing and running tests.

1.  **Install pytest:** If you haven't already, install `pytest`.
    ```bash
    pip install pytest pytest-cov # pytest-cov for coverage reports
    ```
2.  **Run Tests:** Navigate to the repository root and run `pytest`. The `-v` flag increases verbosity. Using `pytest-cov` allows generating [code coverage](https://coverage.readthedocs.io/en/7.5.4/) reports.
    ```bash
    # Run tests with verbosity
    python -m pytest tests -v

    # Run tests and generate a coverage report
    python -m pytest --cov=src tests -v
    ```

### Option 2: Using `unittest` (Built-in)

If you prefer to avoid installing external dependencies for basic testing, you can use Python's standard [unittest](https://docs.python.org/3/library/unittest.html) library.

1.  **Run Tests:** Use the `unittest` command-line interface to discover and run tests within the `tests` directory.
    ```bash
    python -m unittest discover tests -v
    ```

### Notes

-   **Recommendation:** We generally recommend `pytest` due to its powerful features like fixtures, parameterized testing, and extensive plugin ecosystem, which often lead to more readable and maintainable tests.
-   **Simplicity:** `unittest` is readily available in any standard Python installation, making it a straightforward option if external dependencies are a concern.
-   **CI Integration:** These tests are typically integrated into [Continuous Integration (CI)](https://github.com/features/actions) pipelines to automatically validate changes before they are merged, ensuring project stability. See the [Ultralytics contributing guide](https://docs.ultralytics.com/help/contributing/) for more details on our development process.

Regularly running these tests is essential for maintaining the high quality and reliability expected of [Ultralytics](https://www.ultralytics.com/) projects.

## 🤝 Contributing

Contributions to enhance our test suite are welcome! If you find areas lacking coverage or identify new test cases, please feel free to submit a pull request. Ensure your contributions adhere to our coding standards and pass all existing tests. Thank you for helping improve the project!
