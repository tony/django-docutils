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

## Codebase map

The Django-facing entry points are the template tag and filter in
`django_docutils.templatetags.django_docutils`, the template backend in
`django_docutils.template`, and `DocutilsView` in `django_docutils.views`.
They all hand source to the publisher helpers in `django_docutils.lib`, where
roles, directives, transforms, writers, settings, and sanitization are applied.

## Running tests

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

## Building docs

```console
$ just build-docs
```

Run Sphinx doctests:

```console
$ just -f docs/justfile doctest
```

Live reload:

```console
$ just start-docs
```

Before committing, run the full local gate from the repository root:

```console
$ rm -rf docs/_build
$ uv run ruff check . --fix --show-fixes
$ uv run ruff format .
$ uv run mypy .
$ uv run py.test --reruns 0 -vvv
$ just build-docs
```
