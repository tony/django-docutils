# AGENTS.md

django-docutils renders reStructuredText through Django: a `{% rst %}`
template tag and filter, a `DocutilsTemplates` template-engine backend, and
a `DocutilsView` class-based view, all built on docutils publisher helpers
with Django-facing roles, directives, writers, and a sanitizer.

Follow the conventions already in the tree, and keep a change scoped to what was
asked for.

## What is here

| Path | What it is |
| ---- | ---------- |
| `src/django_docutils/templatetags/django_docutils.py` | `{% rst %}` tag and the deprecated `rst` filter |
| `src/django_docutils/template.py` | `DocutilsTemplates` template-engine backend |
| `src/django_docutils/views.py` | `DocutilsView` / `DocutilsResponse` |
| `src/django_docutils/lib/publisher.py` | doctree and HTML rendering helpers |
| `src/django_docutils/lib/sanitize.py` | HTML sanitizer; runs after all transforms |
| `src/django_docutils/lib/settings.py` | resolves `DJANGO_DOCUTILS_LIB_RST` / `_TEXT` |
| `src/django_docutils/lib/{roles,directives,transforms,writers}/` | docutils extension points |
| `tests/` | pytest-django suite; `tests/settings.py` is `DJANGO_SETTINGS_MODULE` |
| `docs/` | Sphinx (MyST) documentation |
| `scripts/runtime_dep_smoketest.py` | verifies runtime deps are complete outside dev groups |
| `CHANGES` | changelog; included verbatim as the docs changelog page |

## Which policy applies

- Documentation, user-facing text, `CHANGES`, commit messages, docstrings,
  and source comments:
  [.github/WRITING.md](.github/WRITING.md)
- Environment, the gates, tests, documentation builds, releases, and pull
  requests: [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)

Each of those is the single home for its subject. Where a rule seems to be
stated twice, the file listed above is the one that governs.

## Change discipline

- Make the smallest coherent change that solves the verified problem; keep
  unrelated cleanup out of it.
- Reuse an existing file, helper, API, or test before adding a new one.
- Add a file only for a durable boundary — a distinct responsibility,
  independent reuse, or splitting an oversized module — not for a single-use
  helper or a one-line re-export.
- Add a test for every user-visible behaviour change, and a `CHANGES` entry for
  every change to the public API, CLI, configuration, or output.
- A passing gate is evidence only once it has been shown capable of failing.
  Pair a new test with a deliberate break that proves it bites.

Rendering is locked down by default for untrusted reStructuredText — read
[Security](docs/topics/security.md) before changing `lib/sanitize.py` or the
`SAFE_DOCUTILS_DEFAULTS` / `PROTECTED_DOCUTILS_DEFAULTS` baselines in
`lib/settings.py`.

## References

- Documentation: <https://django-docutils.git-pull.com>
- Changelog: `CHANGES`
- PyPI: <https://pypi.org/project/django-docutils/>
- Django docs: <https://docs.djangoproject.com/>
- Docutils: <https://docutils.sourceforge.io/docs/>
