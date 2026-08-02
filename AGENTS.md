# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, etc.) when working with code in this repository. CLAUDE.md is a symlink to this file.

Autoimport (`ultralytics-autoimport` on PyPI, AGPL-3.0) is a lightweight Python package for deferring imports until first use through the `lazy` context manager and `LazyLoader` module proxy. Supported Python versions are 3.8 through 3.14.

## Core Principles (CRITICAL)

**Less is more. The simplest solution is the best solution.** The action hierarchy for every change: **Delete > Replace > Add**.

1. **Solve at the owner**: Put behavior in the code path that owns or observes it. For fixes, never guard a symptom with a staleness check, initialization flag, skip-first-call branch, or `try/except` around broken logic; relocate the trigger and delete the wrong path. For features, extend the existing owner rather than creating a parallel abstraction.
2. **Search and reuse first**: Search the whole repository before creating a feature, component, helper, workflow, or utility. Reuse or adapt what exists, consolidate in-scope duplication in the shared owner, and delete duplicate paths. Three similar lines beat a helper nobody else calls.
3. **Delete and modify existing code before creating new code**: Bugfixes are net-negative by default unless deletion and relocation are demonstrably impossible. A new file must first prove it cannot fit cleanly in an existing owner.
4. **Keep scope minimal**: Implement only the simplest complete solution. Avoid impossible-state handling, speculative flags, compatibility shims, policy scaffolding, and unrelated cleanup. Tests are out of scope by default — rely on existing coverage and focused validation; only an uncovered, high-risk regression path justifies minimal new test code.
5. **Ship zero-regression, production-ready changes**: Understand what you remove instead of retaining broken code as insurance. Remove unused imports, functions, types, files, and comments; run relevant cleanup checks; and thoroughly debug and validate the changed owner. Do not break existing features or workflows unless the PR intentionally removes them with evidence.

**Review gate:** for every addition, the reviewer decides whether deleting or changing existing code would have fixed the problem instead — if it would, that is a blocking finding. A missing or thin PR description is never itself a finding.

NEVER push to `main`. NEVER force push. Always start work in a new git worktree (`git worktree add`) on a feature branch and open a PR — never edit the primary checkout directly, it may hold in-flight work.

## PR Workflow

After opening a PR:

1. Wait for the automated PR review and auto-format commit from Ultralytics Actions (`format.yml`), then pull and address every finding.
2. Review the full diff in-session against the Core Principles, performance, and the review gate above, then batch the fixes into one commit and push. After each round of bot or human commits, pull and resume the same reviewer on `<last-reviewed-sha>..HEAD` plus anything that delta could have invalidated. Repeat until the local head matches the live head.
3. Hand off or merge only on a clean final pass: one cold full-diff review returning LGTM with no findings, on a head that is still live at merge time.
4. Never fight other commits: Ultralytics Actions pushes auto-format and header commits, and multiple users may work on the same PR. `git pull --rebase` before pushing; never reset or revert commits you did not author.
5. After the PR merges, clean up: remove local worktrees and branches for it, then `git checkout main && git pull`.

## Commands

```bash
# Development install
uv pip install -e ".[dev]"

# Full test suite (matches ci.yml)
python -m unittest discover tests -v

# Single test module
python -m unittest tests/test_autoimport.py -v

# Format and lint (source of truth: pyproject.toml, line length 120)
ruff format . && ruff check --fix .
```

- CI (`ci.yml`) runs the full `unittest` suite on Python 3.8, 3.13, and 3.14 across Ubuntu, macOS, and Windows.
- `pyproject.toml` configures pytest doctests, but CI uses `unittest`; validate with the CI command above unless the change specifically requires pytest behavior.

## Architecture

- `autoimport/main.py` owns all lazy-import behavior. `lazy` temporarily replaces `builtins.__import__`, and `LazyLoader` imports and caches the real module on first attribute access.
- `autoimport/__init__.py` defines the public API (`LazyLoader`, `lazy`) and package version.
- `tests/test_autoimport.py` covers lazy import behavior with the standard-library `unittest` framework.
- `.github/workflows/` owns CI, formatting, CLA checks, and PyPI publication.

## Conventions

- Every Python and workflow file starts with `# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license`; Ultralytics Actions adds headers automatically, so do not add or revert them manually.
- Use Google-style docstrings and keep lines within the Ruff-configured 120-character limit.
- Preserve compatibility across Python 3.8 through 3.14: do not introduce syntax or standard-library APIs outside that range.
- Keep the public API in `autoimport/__init__.py` deliberate and minimal. Adding or renaming an exported symbol requires updating `__all__` and validating import behavior.
- Releases are version-driven: bump `__version__` in `autoimport/__init__.py`; pushes to `main` by @glenn-jocher run `publish.yml`, which tags and publishes only when that version is newer than PyPI.
