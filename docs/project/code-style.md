# Code Style

## Formatting

django-docutils uses [ruff](https://github.com/astral-sh/ruff) for both linting and formatting.

```console
$ uv run ruff format .
```

```console
$ uv run ruff check . --fix --show-fixes
```

## Type Checking

Strict [mypy](https://mypy-lang.org/) with [django-stubs](https://github.com/typeddjango/django-stubs) is enforced across `src/` and `tests/`.

```console
$ uv run mypy
```

## Docstrings

Follow [NumPy-style docstrings](https://numpydoc.readthedocs.io/en/latest/format.html) for all public functions and methods.

## Imports

- Always include `from __future__ import annotations` at the top of Python files.
- Use `import typing as t` and access via namespace: `t.Optional`, `t.Dict`, etc.
