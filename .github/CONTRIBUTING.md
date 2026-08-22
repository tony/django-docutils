# Contributing

Thanks for looking. Bug reports with a minimal reproduction, and notes on
where the documentation misled you, are the most useful thing you can send.

How this project writes prose — README, `CHANGES`, commit messages,
docstrings, and source comments — is set out separately in
[WRITING.md](WRITING.md). Read that before changing any of it. The
constraints every change is held to, and the map of what is where, are in
[AGENTS.md](../AGENTS.md).

## Getting set up

Install [git](https://git-scm.com/) and [uv](https://github.com/astral-sh/uv).

```console
$ git clone https://github.com/tony/django-docutils.git
```

```console
$ cd django-docutils
```

```console
$ uv sync --all-extras --dev
```

## Codebase map

The Django-facing entry points are the template tag and filter in
`django_docutils.templatetags.django_docutils`, the template backend in
`django_docutils.template`, and `DocutilsView` in `django_docutils.views`.
They all hand source to the publisher helpers in `django_docutils.lib`,
where roles, directives, transforms, writers, settings, and sanitization are
applied.

## The gates

Format:

```console
$ uv run ruff format .
```

Lint:

```console
$ uv run ruff check . --fix --show-fixes
```

Type-check:

```console
$ uv run mypy
```

Test:

```console
$ uv run pytest
```

Documentation is a gate, not a courtesy. Docstring examples, and `.rst`/`.md`
pages under `testpaths` (`docs`, `tests`, `scripts`), are executed by
`pytest`; the doctest flags live in `pyproject.toml`, so there is no
separate doctest step and a green `pytest` is the proof. Which blocks
qualify, and the one mistake that silently removes a test, are in
[WRITING.md](WRITING.md#documented-examples-that-run).

Every module opens with `from __future__ import annotations` — ruff's
`isort` `required-imports` fails the lint gate otherwise. Import the stdlib
`typing` module as `import typing as t` and access members through the
namespace (`t.Any`, not `from typing import Any`); third-party packages may
use `from x import y`.

Before claiming a test or a gate works, show it failing. A gate that has
never been red is an assumption.

## Tests

The suite is pytest-django; `DJANGO_SETTINGS_MODULE` is `tests.settings`
(set in `pyproject.toml`, with `django_find_project = false`). Reach for
`pytest.mark.django_db` only when a test actually touches Django models —
most tests here are pure functions and need no database. Keep RST snippets
in a test small and realistic; put a complex rendering scenario in its own
dedicated test under `tests/` rather than growing one snippet to cover it.

Run a single file:

```console
$ uv run pytest tests/test_template.py
```

Watch tests on change:

```console
$ uv run ptw .
```

CI also runs a runtime-dependency smoke test — it installs only
`[project.dependencies]` into an isolated environment, imports every module,
and renders RST, so anything imported at runtime but declared in a
dependency group (`dev`, `docs`, `testing`, `lint`) fails here instead of on
PyPI. It is skipped by default locally — `conftest.py` skips anything marked
`scripts__runtime_dep_smoketest` unless you ask for it:

```console
$ uv run pytest -m scripts__runtime_dep_smoketest
```

or the isolated form CI runs:

```console
$ uvx --isolated --no-cache --from . python scripts/runtime_dep_smoketest.py
```

Python 3.10 through 3.14 and Django 5.2 through 6.1 are all exercised in CI
(`.github/workflows/tests.yml`); Django 6.x requires Python 3.12+, so the
matrix excludes Python 3.10 against Django 6.0 and 6.1.

## Documentation

Build the Sphinx docs:

```console
$ just build-docs
```

Live-reload while editing:

```console
$ just start-docs
```

A separate, CI-unenforced gate runs any `>>> ` example under `docs/` through
Sphinx's own doctest builder, which pre-imports the names listed in
`docs/conf.py`'s `doctest_global_setup`:

```console
$ just -f docs/justfile doctest
```

## Releasing

Never create tags. Never push tags. The owner handles tagging and tag
pushes, because a tag triggers the publish workflow. See
[Release commits](WRITING.md#release-commits).

django-docutils is pre-1.0: minor version bumps may include breaking
changes, so consumers pin `>=0.x,<0.y`. Releasing is the owner's process —
update `CHANGES`, bump the version in `src/django_docutils/__about__.py`,
commit as `Tag v<version>`, tag `v<version>`, and push both the commit and
the tag. Pushing a tag matching `refs/tags/*` runs the `release` job in
`.github/workflows/tests.yml`, which builds the package and publishes to
PyPI through trusted publishing — no token is stored in the repository.

## Pull requests

One subject per pull request. Unrelated cleanup found along the way belongs
in its own commit, and usually in its own pull request.

Discuss a substantial change via an issue before making it.

Commit format is in [WRITING.md](WRITING.md#commits).

A pull request needs the sign-off of one other developer before merging;
without merge permission, ask a maintainer to merge it for you.

## Decorum

- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of
  personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should
  always assume good intentions.
- Behaviour which can be reasonably considered harassment will not be
  tolerated.

Based on [Ruby's Community Conduct Guideline](https://www.ruby-lang.org/en/conduct/).

## Security

Please do not open a public issue for a vulnerability. This repository has
no `SECURITY.md`; use GitHub's private
[vulnerability reporting](https://github.com/tony/django-docutils/security/advisories/new)
instead.
