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
just test
# or
uv run pytest

# Run a single test file
uv run pytest tests/test_template.py

# Run docs/doctests
uv run pytest docs

# Watch tests
just start          # runs ptw with default args
uv run ptw .        # explicit watcher
```

### Linting and Type Checking

```bash
# Ruff lint
just ruff
# or directly
uv run ruff check .

# Format code
just ruff-format
uv run ruff format .

# Ruff with fixes
uv run ruff check . --fix --show-fixes

# Type checking
just mypy
uv run mypy `find . -type f -not -path '*/.*' | grep -i '.*[.]py$'`

# Watchers
just watch-ruff
just watch-mypy
```

### Documentation

```bash
# Build docs (Sphinx)
just build-docs

# Live-reload docs
just start-docs

# Edit docs assets/design
just design-docs
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

### Doctests

**All functions and methods MUST have working doctests.** Doctests serve as both documentation and tests.

**CRITICAL RULES:**
- Doctests MUST actually execute - never comment out function calls or similar
- Doctests MUST NOT be converted to `.. code-block::` as a workaround (code-blocks don't run)
- If you cannot create a working doctest, **STOP and ask for help**

**Available tools for doctests:**
- `doctest_namespace` fixtures: `tmp_path`
- Django `settings` fixture (from pytest-django)
- Ellipsis for variable output: `# doctest: +ELLIPSIS`
- Update `conftest.py` to add new fixtures to `doctest_namespace`

**`# doctest: +SKIP` is NOT permitted** - it's just another workaround that doesn't test anything. Use fixtures properly.

**Using fixtures in doctests:**
```python
>>> from django_docutils.lib.publisher import publish_html_from_source
>>> rst_source = "Hello **world**"
>>> html = publish_html_from_source(rst_source)  # doctest: +ELLIPSIS
>>> 'world' in html
True
```

**When output varies, use ellipsis:**
```python
>>> from django_docutils.lib.publisher import publish_parts_from_source
>>> parts = publish_parts_from_source("Test")  # doctest: +ELLIPSIS
>>> 'body' in parts
True
```

### Logging Standards

These rules guide future logging changes; existing code may not yet conform.

#### Logger setup

- Use `logging.getLogger(__name__)` in every module
- Add `NullHandler` in library `__init__.py` files
- Never configure handlers, levels, or formatters in library code — that's the application's job

#### Structured context via `extra`

Pass structured data on every log call where useful for filtering, searching, or test assertions.

**Core keys** (stable, scalar, safe at any log level):

| Key | Type | Context |
|-----|------|---------|
| `django_app` | `str` | Django app label |
| `django_setting` | `str` | settings key accessed |
| `django_rst_source_len` | `int` | RST source length |
| `django_publisher_part` | `str` | part name (html, body) |

Treat established keys as compatibility-sensitive — downstream users may build dashboards and alerts on them. Change deliberately.

#### Key naming rules

- `snake_case`, not dotted; `django_` prefix
- Prefer stable scalars; avoid ad-hoc objects

#### Lazy formatting

`logger.debug("msg %s", val)` not f-strings. Two rationales:
- Deferred string interpolation: skipped entirely when level is filtered
- Aggregator message template grouping: `"Running %s"` is one signature grouped ×10,000; f-strings make each line unique

When computing `val` itself is expensive, guard with `if logger.isEnabledFor(logging.DEBUG)`.

#### stacklevel for wrappers

Increment for each wrapper layer so `%(filename)s:%(lineno)d` and OTel `code.filepath` point to the real caller. Verify whenever call depth changes.

#### Log levels

| Level | Use for | Examples |
|-------|---------|----------|
| `DEBUG` | Internal mechanics | Template rendering, processor pipeline steps |
| `INFO` | Lifecycle, user-visible operations | Extension loaded, configuration applied |
| `WARNING` | Recoverable issues, deprecation | Deprecated setting, missing optional dependency |
| `ERROR` | Failures that stop an operation | Rendering failed, invalid configuration |

#### Message style

- Lowercase, past tense for events: `"extension loaded"`, `"rendering failed"`
- No trailing punctuation
- Keep messages short; put details in `extra`, not the message string

#### Exception logging

- Use `logger.exception()` only inside `except` blocks when you are **not** re-raising
- Use `logger.error(..., exc_info=True)` when you need the traceback outside an `except` block
- Avoid `logger.exception()` followed by `raise` — this duplicates the traceback. Either add context via `extra` that would otherwise be lost, or let the exception propagate

#### Testing logs

Assert on `caplog.records` attributes, not string matching on `caplog.text`:
- Scope capture: `caplog.at_level(logging.DEBUG, logger="django_docutils.lib.publisher")`
- Filter records rather than index by position: `[r for r in caplog.records if hasattr(r, "django_app")]`
- Assert on schema: `record.django_app == "myapp"` not `"myapp" in caplog.text`
- `caplog.record_tuples` cannot access extra fields — always use `caplog.records`

#### Avoid

- f-strings/`.format()` in log calls
- Unguarded logging in hot loops (guard with `isEnabledFor()`)
- Catch-log-reraise without adding new context
- `print()` for diagnostics
- Logging secret env var values (log key names only)
- Non-scalar ad-hoc objects in `extra`
- Requiring custom `extra` fields in format strings without safe defaults (missing keys raise `KeyError`)

### Git Commit Standards

#### Release commits

Never create tags. Never push tags. The user handles tagging and tag
pushes (tags trigger the CI publish workflow).

Release commit subjects are plain and short: `Tag v<version>`. Put
the detailed why/what in the commit body. Don't use the
`Scope(type[detail]):` format for releases — don't bury the lede.

## Commit Messages

Use conventional, component-scoped subjects:

```
Scope(type[detail]): concise description

why: Impact or necessity
what:
- Specific technical changes (single topic)
```

Commit types: feat, fix, refactor, docs, chore, test, style, py(deps), py(deps[dev]). Keep subject ≤50 chars, body lines ≤72, imperative voice, one blank line between subject and body.

- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[rules])**: Claude Code rules (CLAUDE.md)
- **ai(claude[command])**: Claude Code command changes

## Changelog Conventions

These rules apply when authoring entries in `CHANGES`, which is rendered as the Sphinx changelog page. Modeled on Django's release-notes shape — deliverables get titles and prose, not bullets.

**Release entry boilerplate.** Every release header is `## django-docutils X.Y.Z (YYYY-MM-DD)`. The file opens with a `## django-docutils X.Y.Z (unreleased)` placeholder block fenced by `<!-- KEEP THIS PLACEHOLDER ... -->` and `<!-- END PLACEHOLDER ... -->` HTML comments — new release entries land immediately below the END marker, never above it.

**Open with a multi-sentence lead paragraph.** Plain prose, no italic. Open with the version as sentence subject (*"django-docutils X.Y.Z ships …"*) so the lead is self-contained when excerpted. Two to four sentences telling the reader what shipped and who cares — user-visible takeaways, not internal mechanism. Cross-reference detail docs with `{ref}` to keep the lead compact.

**Lead paragraphs are release-time material — off-limits to branches and PRs.** The unreleased entry carries no lead paragraph and no version summary: sections only (`### Breaking changes`, `### What's new` deliverables, `### Fixes`, …). Speaking for the release — what the version "is", "ships", or "focuses on" — is presumptuous before its scope is final; only the person cutting the release writes that, and only when the user explicitly asks to release. Never write or edit a lead from a feature branch, and never ask or imply that a release should happen.

**Each deliverable is a section, not a bullet.** Inside `### What's new`, every distinct deliverable gets a `#### Deliverable title (#NN)` heading naming it in user vocabulary, followed by 1-3 prose paragraphs explaining what shipped. Don't wrap a paragraph in `- ` — bullets are for enumerable lists, not paragraph containers. Cross-link detail docs (`See {ref}\`foo\` for details.`) so prose stays focused.

**The deliverable test.** Before writing an entry, ask: "What's the deliverable, in user vocabulary?" If you can't answer in one sentence, the entry isn't ready. Mechanism (helper internals, byte counters, schema-validation locations) belongs in PR descriptions and code comments, not the changelog.

**Fixed subheadings**, in this order when present: `### Breaking changes`, `### Dependencies`, `### What's new`, `### Fixes`, `### Documentation`, `### Development`. Dev tooling (helper scripts, internal automation) lives under `### Development`. For breaking changes, show the migration path with concrete inline code (e.g. a `# Before` / `# After` fenced code block). Dependency floor bumps use the form ``Minimum `pkg>=X.Y.Z` (was `>=X.Y.W`)``.

**PR refs `(#NN)`** sit in each deliverable's `####` heading.

**When bullets are appropriate.** Catch-all sections (`### Fixes`, occasionally `### Documentation`) with 3+ genuinely small items use bullets — one line each, never paragraphs. If a bullet swells past two lines, promote it to a `#### Title (#NN)` heading with prose body.

**Anti-patterns.**

- Fragile metrics: token ceilings, third-party version pins, percent benchmarks, exact byte counts. Describe the *capability*, not the math.
- Internal jargon: private symbols (leading-underscore identifiers), algorithm names exposed for the first time, backend scaffolding.
- Walls of text dressed up as bullets.
- Buried breaking changes — they get their own subheading at the top of the entry.

**Always link autodoc'd APIs.** Any class, method, function, exception, or attribute that has its own rendered page must be cited via the appropriate role (`{class}`, `{meth}`, `{func}`, `{exc}`, `{attr}`) — never with plain backticks. Doc pages without explicit ref labels use `{doc}`. Plain backticks are correct for code syntax, env vars, parameter names, and file paths that aren't doc pages — anything without an autodoc destination.

**MyST roles.** Class references use `{class}`, methods use `{meth}`, functions use `{func}`, exceptions use `{exc}`, attributes use `{attr}`, internal anchors use `{ref}`, doc-path links use `{doc}`.

**Summarization style.** When a user asks "what changed in the latest version?" or similar, lead with the entry's lead paragraph (paraphrased if needed), followed by each `####` deliverable heading under `### What's new` with a one-sentence summary. Cite `(#NN)` only if the user asks for source links. Don't invent versions, dates, or numbers not present in `CHANGES`. Don't quote line numbers or file offsets — those shift as the file evolves.

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

## AI Slop Prevention

Treat AI slop as **review-hostile noise**, not as proof that text or
code is wrong. The goal is to maximize information density by removing
artifacts that make the repository harder to trust or navigate.

### The Anti-Slop Rubric

Before committing, audit all AI-assisted changes for these noise
patterns:

- **AI Signatures:** Remove "Generated by", footers, conversational
  filler ("Certainly!", "Here is..."), unexplained emojis (🤖, ✨), and
  AI-tool metadata.
- **Brittle References:** Avoid hard-coded line numbers, fragile
  file/test counts, dated "as of" claims, bare SHAs, and local
  absolute paths unless they are strict evidentiary artifacts (e.g.,
  benchmark logs).
- **Diff Narration:** Do not restate what moved, was renamed, or was
  removed in artifacts the downstream reader holds: code, docstrings,
  README, CHANGES, PR descriptions, or release notes. The diff and
  commit message already carry this history.
- **Branch-Internal Narrative:** Do not mention intermediate branch
  states, abandoned approaches, or "no longer" behavior unless users
  of a published release actually experienced the old state (**The
  Published-Release Test**).
- **Low-Value Scaffolding:** Remove ownerless TODOs (`TODO: revisit`),
  unused future-proofing, debug artifacts, and defensive wrappers that
  do not protect a currently reachable failure mode.
- **Prose Inflation:** Replace generic AI "tells" like *comprehensive,
  robust, seamless, production-ready, leverage, delve, tapestry,* and
  *best practices* with concrete descriptions of behavior,
  constraints, or trade-offs.

### Preservation & Context

**When unsure, leave the text in place and ask.** Subjective cleanup
must never be a reason to remove load-bearing rationale.

- **Preserve the "Why":** You MUST NOT delete comments that document
  invariants, protocol constraints, platform quirks, security
  boundaries, and upstream workarounds.
- **Evidence is Immune:** Preserve exact counts, dates, and SHAs when
  they serve as evidence in benchmark results, release notes, stack
  traces, or lockfiles.
- **Behavior Over Inventory:** A useful description explains what
  changed for the *system or user*; it does not provide an inventory
  of files or functions the diff already shows.

### The Published-Release Test

Long-running branches accumulate tactical decisions — renames,
refactors, attempts-then-reverts. When deciding what counts as
branch-internal, use trunk or the parent branch as the baseline — not
intermediate states inside the current branch. Ask:

> Did users of the most recently published release ever experience
> this old name, old behavior, or bug?

If the answer is **no**, it is branch-internal narrative. Move it to
the commit message and describe only the final state in the artifact.

**Keep in shipped artifacts:**
- Deprecations and migration guides for symbols that actually shipped.
- `### Fixes` entries for bugs that affected users of a published
  release.
- Comments explaining *why the current code looks this way*
  (invariants, platform quirks) that make sense to a reader who never
  saw the previous version.

### Cleanup in Hindsight

When applying these rules retroactively from inside a feature branch,
first establish scope by diffing against the parent branch (or trunk)
to identify which commits this branch actually introduced. Then:

- **In-branch commits:** Prompt the user with two options: `fixup!`
  commits with `git rebase --autosquash` to address each causal commit
  at its source, or a single cleanup commit at branch tip.
- **Trunk/Parent commits:** Default to leaving them alone. Act only on
  explicit user instruction. If the user opts in, fold the cleanup
  into a single commit at branch tip; do not rewrite shared history.
- **Scope guard:** If cleaning prior slop would touch a colleague's
  work or expand the branch beyond its stated goal, stay in lane:
  protect the current goal and leave prior slop alone.

