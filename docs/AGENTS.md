# Documentation voice

This file covers the *voice* of prose under `docs/` — how to frame a
page so a reader meets the idea before its settings surface. It
complements the repository-root `AGENTS.md`, which already governs
doctests, changelog conventions, and MyST roles. When the two overlap,
the root file wins; this one only answers the question it leaves open:
how should the prose sound?

## Who you are writing for

The default reader is a Django developer who wants reStructuredText
rendered in their site — through the `{% rst %}` template tag, the
`rst` filter, or `DocutilsView`. They are fluent in Django —
templates, `INSTALLED_APPS`, the `TEMPLATES` setting, class-based
views — but you cannot assume they know docutils: the publisher,
roles, directives, transforms, writers, or even reStructuredText
itself (that is why `docs/topics/what_is_docutils.md` exists).

A second, smaller reader extends the pipeline: custom roles and
directives registered through `DJANGO_DOCUTILS_LIB_RST`, transforms,
the publisher helpers in `django_docutils.lib`, or contributing.
Serve them too, but mark their material opt-in ("for the rarer
cases", "advanced") so the default reader knows they can stop. Never
make the common case pay a comprehension tax for the advanced one.

## Voice

- **Second person, present tense, active.** "You load the tag", not
  "The markup is rendered". Address the reader who is doing the thing.
- **Concept before settings surface.** Open by saying what the
  feature *is* and what it does for the reader. The
  `DJANGO_DOCUTILS_LIB_RST` keys — the dict shape, the flags — are
  the last detail they need, not the first. A page that opens with
  "set these keys" has buried the idea under its mechanics.
- **Say when they can stop.** Lead with the default and the
  reassurance: `INSTALLED_APPS` plus `{% rst %}` covers most sites,
  the locked-down rendering defaults work, the advanced parts are
  optional. Let a skimmer leave after one paragraph.
- **Grant permission, don't demand attention.** "Reach for this
  when…", "for the rarer cases" — tell readers they're in the right
  place without implying they must read on.
- **Progressive disclosure.** Order by how many readers need it: the
  template tag with defaults → the one setting a few will tune → the
  template-engine backend and `DocutilsView` → custom roles and
  publisher helpers. Each step is for a smaller audience than the last.
- **Lean on the pipeline.** The reader thinks template in, HTML out;
  the docs' mental model is the chain underneath: a tag, filter, or
  view hands source to the publisher, roles / directives / transforms
  run, and the sanitizer runs last. Reinforce that chain when you
  explain where a feature hooks in.
- **Name the trade-off.** If an option costs something — the trusted
  opt-in buys `.. include::` and `.. raw::` for static RST that ships
  with the app, at the price of being unsafe for anything
  user-authored — say so plainly. State it; don't sell it.
- **Frame by concept, not by mechanism.** Don't headline a feature by
  its settings key in prose; `allow_unsafe_docutils_settings` names
  the implementation surface, which is the reader's last concern.
  Name the concept — "Trusted RST opt-in" — and keep the key in the
  code block or the API reference.

## Examples that run

Sphinx doctest examples run through `just -f docs/justfile doctest`, and
autodoc examples receive the imports configured in `docs/conf.py`. Pytest does
not collect Markdown pages by itself; fenced examples that cannot be doctested
belong in focused tests under `tests/`, such as the docs-snippet contract tests.
When a docs page uses a `>>>` example, spell out any imports that are not in the
Sphinx doctest global setup.

Most examples in these docs never execute: fenced `django` template
blocks, settings dicts, and rendered-HTML output are prose to pytest.
They are still claims about real behavior — check them against a
passing test under `tests/` before you change them.

## What stays precise

Warm the framing, never the facts. Settings dicts, allowed-scheme
lists, writer tables, exact rendered-HTML output, and class or
function cross-references carry meaning in their exact form — leave
them alone. The friendly voice belongs in the sentences *around* a
precise block, introducing it, not inside it paraphrasing it into
vagueness.

## Cross-references

Point the advanced reader at the deep-dive rather than inlining it,
and put the link where their interest peaks — on the phrase that made
them curious ("custom pipelines", "user-authored markup") — not as a
standalone footnote the eye skips. Use the MyST roles listed in the
root `AGENTS.md` (`{class}`, `{meth}`, `{func}`, `{exc}`, `{attr}`,
`{ref}`, `{doc}`). A `{ref}` must match its target's anchor exactly —
anchors mix underscore and hyphen forms across pages (`template_tag`,
`what-is-docutils`). `just build-docs` catches a broken
cross-reference; the doctests do not — so build the docs before you
commit.

Link the first prose mention of any symbol that has a useful destination on
that page. This includes Python objects, django-docutils APIs, Django and
docutils concepts, topic pages, and external tools or projects. Use the most
specific target available: `{class}`, `{meth}`, `{func}`, `{mod}`, `{exc}`, or
`{attr}` for API objects; `{ref}` or `{doc}` for documentation pages and
section anchors; and a Markdown link or reference link for external projects.
After the first linked mention on a page, later mentions can stay plain unless
the distance or context makes another link useful.

Do not rely on a later reference section to satisfy the first-mention rule. If
the first occurrence would be a heading, grid-card teaser, or introductory
sentence, link that occurrence or retitle the heading so the first prose mention
can carry the link. Leave command examples, code blocks, and literal
configuration values as code; link the surrounding prose instead.

## A page that does this

`docs/topics/security.md` is the worked example: a concept-first intro
that says what the renderer does and for whom before any setting, a
"Default posture" section that leads with what you get without
configuration, sections ordered by shrinking audience (defaults → how
sanitization runs → trusted opt-in → URI schemes → operational
advice), an honest trade-off stated plainly ("They reduce risk; they
do not make untrusted markup safe"), the opt-in named by concept with
its key kept inside the code block, and precise settings blocks and
scheme lists left exact. Read it before reshaping another page.

## Before you commit

- Does the page open with what the feature *is*, or with how to
  configure it?
- Can a reader who needs only the locked-down defaults stop after the
  first paragraph?
- Is anything headlined by a settings key that should be named by
  concept instead?
- Are the advanced and pipeline-level parts clearly marked opt-in?
- Did you leave every settings block, output block, table, and
  cross-reference exact — and do any `>>>` examples pass
  `just -f docs/justfile doctest`?
- Did `just build-docs` stay clean — no new warning, no broken
  cross-reference?
