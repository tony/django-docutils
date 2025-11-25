# AGENTS.md

This file provides guidance to AI agents (including Claude Code, Cursor, and other LLM-powered tools) when working with code in this repository.

## CRITICAL REQUIREMENTS

### Test Success
- ALL tests MUST pass for code to be considered complete and working
- Never describe code as "working as expected" if there are ANY failing tests
- Even if specific feature tests pass, failing tests elsewhere indicate broken functionality
- Changes that break existing tests must be fixed before considering implementation complete
- A successful implementation must pass linting, type checking, AND all existing tests

## Project Overview

django-docutils is a Django integration that renders docutils/reStructuredText content inside Django templates, views, and template engines. The project dogfoods gp-libs' Sphinx/pytest tooling while focusing on Django-facing helpers.

Key features:
- `{% rst %}` template tag and `rst` filter to render RST to HTML
- Django template engine backend (`DocutilsTemplates`) to render `.rst` files as templates
- Class-based view (`DocutilsView`) and response class for serving RST-backed pages
- Docutils publisher helpers with custom writers, roles, directives, and transforms (e.g., TOC)
- Settings hooks for docutils options and extension registration

## Development Environment

This project uses:
- Python 3.10+
- Django 4.2/5.1/5.2
- [uv](https://github.com/astral-sh/uv) for dependency management
- [ruff](https://github.com/astral-sh/ruff) for linting/formatting
- [mypy](https://github.com/python/mypy) with `django-stubs` for typing
- [pytest](https://docs.pytest.org/) + `pytest-django` + gp-libs doctest tooling
- [Sphinx](https://www.sphinx-doc.org/) (furo theme) for documentation

## Common Commands

### Setting Up Environment

```bash
# Install runtime dependencies
uv pip install --editable .
uv pip sync

# Install with development groups (docs, lint, tests)
uv pip install --editable . -G dev
# or selectively
uv pip install --editable . -G docs
uv pip install --editable . -G testing
uv pip install --editable . -G lint
```

### Running Tests

```bash
# Run all tests (includes doctests configured in pyproject)
make test
# or
uv run pytest

# Run a single test file
uv run pytest tests/test_template.py

# Run docs/doctests
uv run pytest docs

# Watch tests
make start          # runs ptw with default args
uv run ptw .        # explicit watcher
```

### Linting and Type Checking

```bash
# Ruff lint
make ruff
# or directly
uv run ruff check .

# Format code
make ruff_format
uv run ruff format .

# Ruff with fixes
uv run ruff check . --fix --show-fixes

# Type checking
make mypy
uv run mypy `find . -type f -not -path '*/.*' | grep -i '.*[.]py$'`

# Watchers
make watch_ruff
make watch_mypy
```

### Documentation

```bash
# Build docs (Sphinx)
make build_docs

# Live-reload docs
make start_docs

# Edit docs assets/design
make design_docs
```

### Development Workflow

Use this loop for every change:

1. **Format First**: `uv run ruff format .`
2. **Run Tests**: `uv run pytest`
3. **Run Linting**: `uv run ruff check . --fix --show-fixes`
4. **Check Types**: `uv run mypy`
5. **Verify Tests Again**: `uv run pytest`

## Code Architecture

django-docutils mirrors Django's template/render pipeline while wrapping docutils:

```
Templates / Views / Template Tags
        └─ Docutils publisher helpers (roles, directives, writers, transforms)
                └─ Docutils settings & utils
```

### Core Modules

1. **Template Engine** (`src/django_docutils/template.py`)
   - `DocutilsTemplates` backend renders `.rst` files through docutils
   - Returns `DocutilsTemplate` objects for Django's template system

2. **Template Tags & Filters** (`src/django_docutils/templatetags/django_docutils.py`)
   - `{% rst %}` tag and `rst` filter render RST to HTML
   - Accepts flags like `toc_only` and `show_title`

3. **Views** (`src/django_docutils/views.py`)
   - `DocutilsView`/`DocutilsResponse` serve RST-backed pages using the docutils engine
   - Supports specifying `rst_name` alongside standard template names

4. **Publisher & Rendering Pipeline** (`src/django_docutils/lib/publisher.py`)
   - Helpers to produce doctrees and HTML parts
   - Registers custom roles/directives (see `lib/roles`, `lib/directives`) and TOC transform

5. **Writers & Transforms** (`src/django_docutils/lib/writers.py`, `lib/transforms/`)
   - Custom HTML writer and TOC handling for Django output

6. **Settings & Types** (`src/django_docutils/lib/settings.py`, `_internal/types.py`)
   - Centralized docutils defaults (`DJANGO_DOCUTILS_LIB_RST`) and typing helpers

## Testing Strategy

django-docutils uses pytest with `pytest-django` and doctest collection enabled via `pyproject.toml`:

- Doctests run on modules and docs (`addopts` includes `--doctest-modules` and `testpaths` includes `docs`)
- `DJANGO_SETTINGS_MODULE=tests.settings` is configured in `pyproject.toml`; use these settings for new tests
- Prefer pytest fixtures and `pytest.mark.django_db` only when touching Django models (most tests are pure functions)
- Use gp-libs doctest helpers when adding RST/markdown doctests in docs
- Keep RST snippets small and realistic; prefer dedicated tests under `tests/` for complex scenarios

### Example Test Usage

```python
def test_rst_tag_renders_toc_only(settings):
    html = publish_html_from_source(SOME_RST, toc_only=True)
    assert "contents" in html
```

## Coding Standards

- Always include `from __future__ import annotations` at the top of Python files
- Prefer namespace imports (`import typing as t`; `import enum`) over `from module import ...`
- Follow NumPy-style docstrings for functions and methods
- Ruff enforces formatting; use `ruff format` before committing
- Type hints are required; keep mypy strictness in mind and add `TypedDict`/`Protocol` as needed
- Use Django utilities (`force_str`, `mark_safe`, `select_template`) instead of reimplementing equivalents

## Commit Messages

Use conventional, component-scoped subjects:

```
Component/File(commit-type[Subcomponent]): Concise description

why: Impact or necessity
what:
- Specific technical changes (single topic)

refs: #issue or links (note BREAKING if applicable)
```

Commit types: feat, fix, refactor, docs, chore, test, style, py(deps), py(deps[dev]). Keep subject ≤50 chars, body lines ≤72, imperative voice, one blank line between subject and body.

## Debugging Tips

When stuck in a loop:
- Acknowledge the loop and list failed attempts
- Minimize to the smallest reproducible case; drop debugging cruft
- Document exact errors and current hypothesis
- Share a portable repro block (code + output) before iterating again

## Notes Content

For files under `notes/**`:
- Be concise and clearly structured with headings and bullet lists
- Use fenced code blocks for code; inline backticks for identifiers
- Avoid redundancy; summarize when possible

## References

- Documentation: https://django-docutils.git-pull.com
- Changelog: `CHANGES`
- PyPI: https://pypi.org/project/django-docutils/
- gp-libs (doctest/Sphinx tooling used here): https://gp-libs.git-pull.com
- Django docs: https://docs.djangoproject.com/
- Docutils: https://docutils.sourceforge.io/docs/
