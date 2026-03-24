# Development

Install [git](https://git-scm.com/) and [uv](https://github.com/astral-sh/uv).

Clone:

```console
$ git clone https://github.com/tony/django-docutils.git
```

```console
$ cd django-docutils
```

Install packages:

```console
$ uv sync --all-extras --dev
```

## Running Tests

```console
$ uv run pytest
```

Run a single test file:

```console
$ uv run pytest tests/test_template.py
```

Watch tests:

```console
$ uv run ptw .
```

## Building Docs

```console
$ uv run sphinx-build docs docs/_build
```

Live-reload:

```console
$ uv run sphinx-autobuild docs docs/_build
```
