# Writing

How this project writes prose, for humans and agents alike. It governs
`README.md`, `CHANGES`, commit messages, docstrings, source comments, error
messages, Django settings documentation, and template tag/filter
documentation — every surface a reader reaches.

For environment setup, the gates, and pull request workflow, see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Voice

Three surfaces, one voice. A docstring says what a caller may rely on; a
`CHANGES` entry says what changed; prose says what happens. All three are
present tense, lead with the thing being described, and stop. Why it was
built that way belongs in the commit message, which is timestamped and
attached to the diff.

The most useful editing operation is deleting the introductory sentence.

Lead with verbs and name concrete things. Put identifiers in backticks.
Prefer short declarative sentences, one operational fact each. Do not
explain Django or docutils to Django developers; do explain this project's
semantics.

Type annotations describe shape. Documentation describes meaning. A sentence
that restates a signature has said nothing.

Use MUST, SHOULD, and MAY only where the normative sense is meant. Say what
actually happens rather than that something is "supported".

| Instead of                       | Prefer                             |
| --------------------------------- | ----------------------------------- |
| "We added…"                       | "`get_docutils_settings` now…"      |
| "New and improved"                | "`DocutilsView` now…"               |
| "powerful", "seamless"            | state the capability                |
| "easily", "simply", "just"        | omit                                |
| "simple", "obvious", "intuitive"  | omit                                |
| "robust"                          | name the failure that is handled    |
| "comprehensive"                   | name what is covered                |
| "production-ready"                | state the guarantee                 |
| "optimized", "blazingly fast"     | give the magnitude                  |
| "various fixes"                   | name the components                 |
| "under the hood"                  | omit unless observable              |
| "please note that", "note that"   | state the fact                      |
| "leverage", "utilize"             | "use"                               |
| "delve into"                      | "read", or omit                     |
| "best practices"                  | name the practice                   |
| "in order to"                     | "to"                                |

## Who you are writing for

The default reader is a Django developer who wants reStructuredText rendered
in their site — through the `{% rst %}` template tag, the `rst` filter, or
`DocutilsView`. They are fluent in Django — templates, `INSTALLED_APPS`, the
`TEMPLATES` setting, class-based views — but do not assume they know
docutils: the publisher, roles, directives, transforms, writers, or even
reStructuredText itself (that is why `docs/topics/what_is_docutils.md`
exists). Serve them first.

A second, smaller reader extends the pipeline: custom roles and directives
registered through `DJANGO_DOCUTILS_LIB_RST`, transforms, the publisher
helpers in `django_docutils.lib`, or the project itself. Serve them too, but
mark their material opt-in — "for the rarer cases", "advanced" — so the
default reader knows they can stop. Never make the common case pay a
comprehension tax for the advanced one.

Rules that follow:

- **Second person, present tense, active.** "You load the tag", not "The
  markup is rendered". Address the reader who is doing the thing.
- **Concept before settings surface.** Open by saying what the feature *is*
  and what it does for the reader. The `DJANGO_DOCUTILS_LIB_RST` keys — the
  dict shape, the flags — are the last detail they need, not the first. A
  page that opens with "set these keys" has buried the idea under its
  mechanics.
- **Say when they can stop.** Lead with the default and the reassurance:
  `INSTALLED_APPS` plus `{% rst %}` covers most sites, the locked-down
  rendering defaults work, the advanced parts are optional. Let a skimmer
  leave after one paragraph.
- **Grant permission, do not demand attention.** "Reach for this when…",
  "for the rarer cases" — tell readers they are in the right place without
  implying they must read on.
- **Progressive disclosure.** Order by how many readers need it: the
  template tag with defaults, then the one setting a few will tune, then the
  template-engine backend and `DocutilsView`, then custom roles and
  publisher helpers. Each step is for a smaller audience than the last.
- **Lean on the pipeline.** The reader thinks template in, HTML out; the
  docs' mental model is the chain underneath: a tag, filter, or view hands
  source to the publisher, roles/directives/transforms run, and the
  sanitizer runs last. Reinforce that chain when explaining where a feature
  hooks in.
- **Name the trade-off.** If an option costs something — the trusted opt-in
  buys `.. include::` and `.. raw::` for static RST that ships with the app,
  at the price of being unsafe for anything user-authored — say so plainly.
  State it; do not sell it.
- **Frame by concept, not by mechanism.** Do not headline a feature by its
  settings key in prose; `allow_unsafe_docutils_settings` names the
  implementation surface, which is the reader's last concern. Name the
  concept — "Trusted RST opt-in" — and keep the key in the code block or the
  API reference.

**What stays precise.** Warm the framing, never the facts. Settings dicts,
allowed-scheme lists, writer tables, exact rendered-HTML output, and class or
function cross-references carry meaning in their exact form — leave them
alone. The friendly voice belongs in the sentences *around* a precise block,
introducing it, not inside it paraphrasing it into vagueness.

## MyST roles and cross-references

Every page under `docs/` is MyST Markdown built by Sphinx with autodoc. Link
the first prose mention of any symbol that has a useful destination on that
page — Python objects, django-docutils APIs, Django and docutils concepts,
topic pages, external tools. Use the most specific target available:
`{class}`, `{meth}`, `{func}`, `{mod}`, `{exc}`, or `{attr}` for API objects;
`{ref}` or `{doc}` for documentation pages and section anchors; a Markdown
link for external projects. After the first linked mention on a page, later
mentions can stay plain unless distance or context makes another link
useful.

Do not rely on a later reference section to satisfy the first-mention rule.
If the first occurrence would be a heading, grid-card teaser, or
introductory sentence, link that occurrence or retitle the heading so the
first prose mention can carry the link. Leave command examples, code blocks,
and literal configuration values as code; link the surrounding prose
instead.

A `{ref}` must match its target's anchor exactly — anchors mix underscore and
hyphen forms across pages (`template_tag`, `what-is-docutils`). `just
build-docs` catches a broken cross-reference; the doctests do not, so build
the docs before committing a page that adds or renames a `(label)=` anchor.

`docs/topics/security.md` is the worked example: a concept-first intro that
says what the renderer does and for whom before any setting, sections
ordered by shrinking audience, an honest trade-off stated plainly ("They
reduce risk; they do not make untrusted markup safe"), an opt-in named by
concept with its key kept inside the code block, and settings blocks and
scheme lists left exact. Read it, and run `just build-docs`, before
reshaping another page.

## README

A README is the shortest path from "what is this?" to competent use, not the
project's autobiography.

The first sentence is a contract. It says what abstraction the reader has
been handed, concretely enough to tell this package apart from the
neighbouring one.

Get to a runnable command or snippet before anything the reader can skip. A
logo, a mission statement, a comparison matrix and three paragraphs of
history in front of the install line all cost the same thing.

State the minimum Python version and Django compatibility in prose, not only
in a bullet. `requires-python` in `pyproject.toml` is the authority; the
README must agree with it.

Name the distribution, the import, and the executable separately wherever
they differ. django-docutils has no executable — the distribution is
`django-docutils`, the import is `django_docutils`.

Examples are executable, not illustrative fiction. Never
`your-command <some-options>`. See
[Documented examples that run](#documented-examples-that-run) for which
blocks are executed and how to write one that qualifies.

Document the semantic model, not the flag list. What a setting's absence
means, what runs before what in the rendering pipeline, and what a locked
default protects against are what a reader cannot get from the source
alone.

State defaults explicitly — defaults are API. State negative guarantees
where they exist: "does not modify your configuration file", "no network
access", "never writes outside the destination". They establish boundaries
faster than any amount of description.

Headings stay conventional and stable, because people deep-link them.
Badges are few and load-bearing.

## Settings

A Django setting is API. `DJANGO_DOCUTILS_LIB_RST` and
`DJANGO_DOCUTILS_LIB_TEXT` are read once at import time (`lib/settings.py`)
and reloaded on Django's `setting_changed` signal — document them like any
other public surface:

- Name the setting exactly, in backticks, matching the constant in
  `lib/settings.py` or the shape in `lib/types.py`.
- State the default that applies when the project never sets it. Unset
  `DJANGO_DOCUTILS_LIB_RST` resolves through `SAFE_DOCUTILS_DEFAULTS`; unset
  `DJANGO_DOCUTILS_LIB_TEXT` is
  `{"uncapitalized_word_filters": []}`.
- Say what an unset value means, not just what a set value does. "Unset
  disables the trusted-content opt-in" says more than "controls whether raw
  HTML is allowed".
- A protected setting (`file_insertion_enabled`, `raw_enabled`,
  `_disable_config`) needs its opt-in flag documented beside it —
  `allow_unsafe_docutils_settings`. Say plainly that setting the protected
  key alone, without the opt-in, is silently overridden by the public
  helpers.
- Link a settings dict's shape to its {class} entry in `lib/types` rather
  than re-describing every key inline.

Security-relevant defaults belong in `docs/topics/security.md` — route there
rather than restating the threat model in a settings reference.

## Template tags and filters

Every documented template tag or filter pairs its Django template source
with the exact HTML it renders, in adjacent fenced blocks (see
`docs/topics/template_tag.md`) — `tests/test_docs_examples.py` renders the
first block and asserts it equals the second, so the two must stay in sync;
editing the shown markup without re-running the suite ships a lie.

State whether a tag or filter is deprecated in the page's opening sentence,
not as a trailing note (see `docs/topics/template_filter.md`) — the same
test file asserts the word "deprecated" appears on that page.

Cross-reference the implementation with `{func}` —
`` {func}`~django_docutils.templatetags.django_docutils.rst` ``, not a bare
backtick — since it renders its own API page.

## Django and Python support

The supported matrix is `pyproject.toml` (`requires-python`, the
`Framework :: Django` classifiers) and
`.github/workflows/tests.yml` (the CI job matrix and its excludes) — read
those, do not guess. django-docutils currently supports Python 3.10 through
3.14 and Django 5.2 through 6.1; Django 6.x requires Python 3.12+, which is
why the CI matrix excludes Python 3.10 against Django 6.0 and 6.1.
`requires-python` is the authority for the Python floor; state the matrix in
prose wherever a reader decides compatibility — the README, the quickstart —
and keep it in agreement.

## Documented examples that run

Examples in this project are tests. This section is the contract for
writing one the test suite can actually see.

**A fence tag is cosmetic. Only a `>>> ` prompt executes.** A block written
as

    ```python
    settings = get_docutils_settings()
    ```

is prose that looks like a test. Nothing collects it, nothing runs it, and
it can be wrong for years. The same block written with a prompt is a test:

    ```python
    >>> settings = get_docutils_settings()
    ```

This is the single most expensive mistake available when editing
documentation, because removing the prompt leaves a green test suite and a
silently deleted test. When editing a file that contains examples, count the
prompts before and after.

**The fence tag is `python`.** Not `pycon`, not bare.

**Where examples run.** `pyproject.toml`'s `testpaths` is
`src/django_docutils`, `tests`, `docs`, and `scripts`, and `addopts` sets
`--doctest-modules`, so pytest collects doctest-style docstrings from every
`.py` file in those paths. `gp-libs` additionally registers a pytest plugin
(`pytest_doctest_docutils`) that collects `>>> ` blocks directly out of any
`.rst` or `.md` file under a collected path — that is what makes a prompted
block on a page under `docs/` executable with no extra configuration.
`README.md` is not in `testpaths`, so a prompt there would render but never
run; the README currently has none.

**No implicit imports.** `conftest.py` defines no `doctest_namespace`
fixture and no `autouse` fixture — an `.rst`/`.md` doctest only receives a
fixture that is `autouse`, and this repository defines none — so nothing is
pre-imported into a doctest's globals. Every example imports what it uses.
`docs/conf.py` sets a `doctest_global_setup` with a long import list, but
that belongs to Sphinx's own `sphinx.ext.doctest` builder
(`just -f docs/justfile doctest`, a gate CI does not run) and has no effect
on the `pytest` collector that gates CI. Do not assume a name from
`doctest_global_setup` is available in a block pytest will run; import it
explicitly.

**`# doctest: +SKIP` is not permitted.** It is a workaround that tests
nothing.

**Do not downgrade a doctest to a non-executed block to make it pass.** A
`.. code-block::` or an unprompted fence does not run. If an example cannot
pass, fix the example or fix the code.

**Option flags.** `ELLIPSIS` and `NORMALIZE_WHITESPACE` are enabled
globally, so `...` elides variable output and whitespace differences do not
fail a comparison. Reach for an inline `# doctest: +FLAG` only for the block
that needs it.

**Docstring examples** use the NumPy `Examples` section:

    Examples
    --------
    >>> from django_docutils.lib.settings import unsafe_docutils_settings_allowed
    >>> isinstance(unsafe_docutils_settings_allowed(), bool)
    True

**Documentation-page examples that render Django templates are checked
twice, differently.** A `>>> ` block on a docs page is a doctest, checked
value-by-value like any other. Separately, `tests/test_docs_examples.py`
parses the fenced `django` and `html` blocks on `docs/topics/template_tag.md`,
`docs/topics/template_filter.md`, `docs/topics/class_based_view.md`, and
`docs/quickstart.md` by language tag and asserts the rendered HTML matches
the shown output byte-for-byte. That contract test is not a doctest and
needs no `>>> ` prompt — but it makes the *fenced, unprompted* example on
those pages load-bearing too: changing the shown template or its HTML
without updating the other half breaks that test.

## The changelog

`CHANGES` is the changelog. Not `CHANGELOG.md`. It is included verbatim as
the docs changelog page (`docs/history.md`), modeled on Django's
release-notes shape: deliverables get titles and prose, not bullets.

**Release entry boilerplate.** Every release header is `## django-docutils
X.Y.Z (YYYY-MM-DD)`. The file opens with a `## django-docutils X.Y.Z
(unreleased)` placeholder fenced by `<!-- KEEP THIS PLACEHOLDER ... -->` and
`<!-- END PLACEHOLDER ... -->` HTML comments — new entries land immediately
below the END marker, never above it.

**Open with a multi-sentence lead paragraph.** Plain prose, no italics. Open
with the version as the sentence subject ("django-docutils X.Y.Z ships …")
so the lead is self-contained when excerpted. Two to four sentences on what
shipped and who cares — user-visible takeaways, not internal mechanism.
Cross-reference detail docs with `{ref}` to keep the lead compact.

**Unreleased entries carry no lead paragraph and no version summary** —
sections only (`### Breaking changes`, `### What's new` deliverables,
`### Fixes`, …). Speaking for a release — what the version "is", "ships", or
"focuses on" — is presumptuous before its scope is final; only the person
cutting the release writes that, and only when the release is actually
happening. Never write or edit a lead paragraph from a feature branch, and
never ask or imply that a release should happen.

**Each deliverable is a section, not a bullet.** Inside `### What's new`,
every distinct deliverable gets a `#### Deliverable title (#NN)` heading
naming it in user vocabulary, followed by one to three prose paragraphs. Do
not wrap a paragraph in `- ` — bullets are for enumerable lists, not
paragraph containers. Cross-link detail docs (`` See {ref}`foo` for
details. ``) so prose stays focused.

**The deliverable test.** Before writing an entry, ask: "What's the
deliverable, in user vocabulary?" If that has no one-sentence answer, the
entry is not ready. Mechanism — helper internals, byte counters,
schema-validation locations — belongs in the pull request description and
code comments, not the changelog.

**Fixed subheadings**, in this order when present: `### Breaking changes`,
`### Dependencies`, `### What's new`, `### Fixes`, `### Documentation`,
`### Development`. Dev tooling (helper scripts, internal automation) lives
under `### Development`. Show a breaking change's migration with concrete
inline `# Before` / `# After` code. Dependency floor bumps use
`` Minimum `pkg>=X.Y.Z` (was `>=X.Y.W`) ``.

**PR refs `(#NN)`** sit in each deliverable's `####` heading.

**When bullets are appropriate.** Catch-all sections (`### Fixes`,
occasionally `### Documentation`) with three or more genuinely small items
use bullets — one line each, never paragraphs. A bullet that swells past two
lines gets promoted to its own `#### Title (#NN)` heading with a prose body.

**Always link autodoc'd APIs.** A class, method, function, exception, or
attribute with its own rendered page is cited with `{class}`, `{meth}`,
`{func}`, or `{exc}` — never a bare backtick. A doc page without a ref label
uses `{doc}`. Plain backticks are correct for code syntax, env vars,
parameter names, and file paths that have no autodoc destination.

**Summarization style.** Asked "what changed in the latest version?", lead
with the entry's lead paragraph (paraphrased if needed), then each `####`
deliverable heading under `### What's new` with a one-sentence summary. Cite
`(#NN)` only if asked for source links. Do not invent versions, dates, or
numbers absent from `CHANGES`; do not quote line numbers or file offsets —
they shift as the file evolves.

**Anti-patterns.** Fragile metrics — token ceilings, third-party version
pins, percent benchmarks, exact byte counts. Describe the capability, not
the math. Private symbols and internal jargon. Walls of text dressed up as
bullets. A breaking change buried mid-entry instead of given its own
subheading at the top.

## Docstrings

The prime directive: never restate the type. The annotation is the source of
truth; the docstring carries what the annotation cannot.

This is documentation debt wearing a docstring:

    def get_scheme(uri: str) -> str:
        """Get the URI's scheme.

        Parameters
        ----------
        uri : str
            The URI.

        Returns
        -------
        str
            The scheme.
        """

Document instead the dimensions the type system cannot encode:

- **Mutation.** What it changes in place.
- **Ownership.** What the caller must close, release, or keep alive.
- **Ordering.** Whether results come back in a guaranteed order.
- **Timing.** What has finished by the time the call returns.
- **Failure.** Which exceptions are raised and what triggers each.
- **Idempotence.** Whether calling twice does anything the second time.
- **Concurrency.** Whether calls are coalesced, queued, or independent.
- **Units and ranges.** What a number means and what values are accepted.
- **Boundary behaviour.** What zero, empty, and the maximum do.
- **Platform.** Behaviour that differs by Django or docutils version.
- **Security boundary.** What is executed, and what is only read — the
  distinction this project's whole sanitizer exists to draw.

The ambiguity worth resolving by example: whether "retry three times" means
three attempts or four. State it.

The first sentence stands alone; tooling truncates there. PEP 257 applies:
triple double quotes, an imperative one-line summary ending in a period, a
blank line before any extended description. Do not repeat an introspectable
signature.

**Classes with fields** — `NamedTuple`, dataclasses — document every field
in an `Attributes` section:

    class ParentNodeClassTuple(t.NamedTuple):
        """Typing for parent node accepting custom arguments.

        Attributes
        ----------
        parent_node_type : type[docutils.nodes.Node | docutils.nodes.Body]
            Parent node class the title must be wrapped in for this entry to apply.
        args : list[str]
            Positional arguments passed to ``starttag``.
        kwargs : dict[str, str]
            HTML attributes passed to ``starttag``.
        close_tag : str | None
            Closing tag emitted after the title, or ``None`` to keep the default.
        """

Autodoc renders every field whether or not you describe it, so an
undocumented `NamedTuple` field ships to the API docs as "Alias for field
number 0" and a dataclass field ships bare. Document all of them — a class
with three fields and two documented still ships a stub for the third.

One docstring dialect per repository, enforced by the linter rather than
relitigated in review. This repository's is NumPy, via ruff's `pydocstyle`
`convention = "numpy"` in `pyproject.toml`.

## Source comments

A comment ships only if it passes all three gates. Fail any: delete or
rewrite. Borderline: delete — borderline means the information is
reconstructible, which is what makes deletion cheap.

**Loss.** Three years from now, would losing this cost a maintainer real
time rediscovering intent, an invariant, a constraint, or a failure mode the
code and tests do not already make obvious?

**Elite.** Would SQLite, Redis, the Go standard library, or CPython write
this comment, at this length? Those projects state the constraint and stop.
They do not argue with an imagined objector.

**Upkeep.** Will it stay true without maintenance? A comment that hand-syncs
a value the code owns — a count, an offset, a line reference, a duplicated
constant — is false the first time that value moves.

### Ceiling

One or two lines. A comment reaching four is either carrying several facts,
in which case split it, or arguing, in which case cut it to the fact.

Rationale, alternatives weighed, and the story of how the code got here
belong in the commit message: timestamped, attached to the exact diff, and
free to maintain.

A comment often holds both a constraint and the deliberation that found it.
Keep the constraint, cut the deliberation. "Runs at most once per second"
survives; "this is the right trade for now" does not.

### Keep

- Why over how: upstream quirks, protocol and compatibility constraints,
  performance tradeoffs still part of the contract.
- Invariants, preconditions, ordering, lifetime, and concurrency
  requirements that types and tests cannot express.
- Code that looks wrong but is not, so a later cleanup does not reintroduce
  the bug.
- A high-level sketch of an algorithm whose local operations do not reveal
  the whole.

### Delete

- Narration of the next lines; code translated into English.
- Restated names, types, defaults, or control flow.
- Values duplicated from the code and hand-synced.
- Justification, hedging, or apology for a choice.
- Speculation about future requirements.
- History version control already holds, including commented-out code.
- Ticket and issue numbers. They say nothing to a reader without tracker
  access, and they rot when the tracker moves. Unfinished work goes in the
  tracker, not the source.
- Transient observations — "currently", "for now", "the latest release" —
  that go stale with no nearby edit.

### The upkeep gate in practice

It reaches values that track our own code. It does not reach frozen external
facts.

Bad (Delete):

    # There are 321 tests to complete for servers.

Good (Keep):

    # CPython < 3.11 has no ExceptionGroup, so this branch stays.

### Documentation exception

Minimal usage examples, and parameter, return, and raises entries on public
API are exempt from the loss gate — they serve the caller, not the
maintainer. NumPy-style `Parameters`, `Returns`, and `Attributes` sections
fall under this exception too: autodoc ships every field whether or not you
describe it. They are exempt from nothing else. Ceiling: a good man page
entry.

## Terminology and capitalization

Pick the domain noun and keep it. If the code calls something a setting, do
not call it an option in one paragraph and a config key in the next.

Stable vocabulary is what makes search, deep links, and an agent's retrieval
work at all.

Say "reStructuredText" on first mention of a page and "RST" after; do not
introduce a third spelling such as "reST" or "rst" in prose.
`docs/topics/faq.md` explains the docutils/reST/RST/reStructuredText naming
for newcomers on purpose — that page is the deliberate exception. Say
"sanitizer" for the runtime behaviour (`sanitize_doctree`,
`SanitizeTransform`) and "sanitization" for the process a section describes.

Python and PyPI keep their own capitalisation. Distribution names are
written as they are published.

Do not write counts into prose — how many symbols exist, how many tests
there are. They go stale silently and no reader needs them. Counts that pin
a fixture or guard an invariant are different, and belong in code.

## Markdown

Prose wraps at 80 columns. Table rows, badge lines, and long links are
exempt, because breaking them harms rendering. A pull request or issue body
does not wrap at all: GitHub renders a single newline as a space in a file
and as a line break in a comment, so a wrapped comment body arrives as
ragged stubs.

GitHub alert blocks — `> [!NOTE]`, `> [!WARNING]` — render as literal text
outside GitHub, so reserve them for at most one load-bearing warning per
document. Under `docs/`, MyST admonitions (`:::{important}`, `:::{seealso}`,
`:::{admonition}`) are the docs-page equivalent — the same
one-load-bearing-warning-per-page discipline applies.

Do not use a local absolute path or an email address in anything published.

## Code blocks

Code blocks are paste-and-run units: pasting one block runs exactly one
intended action. Executed examples are exempt — the test suite runs them,
nobody pastes them.

- **One command per block.** Multiple steps may share a block only when
  explicitly chained with `&&`, `;`, or `\` continuations — the chain is
  then one logical command.
- **Explanations go in prose above the block**, never as `#` comments
  inside it.
- **Command menus are per-command blocks with prose lead-ins**, not tables.
- **Shell commands use the `console` tag with a `$ ` prefix.** This
  separates interactive commands from scripts and enables prompt-aware
  copy.
- **Split long commands with `\`** — one flag or flag+value pair per
  indented continuation line, positional arguments last.

Good — show the last ten commits as a graph:

```console
$ git log \
    --max-count=10 \
    --graph \
    --oneline
```

Bad:

```console
# Show the last ten commits as a graph
$ git log --max-count=10 --graph --oneline
```

## Commits

```
Scope(type[detail]): concise description

why: Explanation of necessity or impact.

what:
- Specific technical changes made
- Focused on a single topic
```

Keep the subject to 50 characters or fewer, excluding any trailing `(#NN)`
pull request reference, and wrap body lines at 72. Separate the `why:` and
`what:` blocks with a blank line.

Routine maintenance commits drop the colon and take a capitalised
description, which is what distinguishes them at a glance in
`git log --oneline`:

```
py(deps[dev]) Bump dev packages
ai(rules[AGENTS]) Judge comments by three gates
```

Everything that changes behaviour keeps the colon.

Common types:

- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **ci**: Workflow and pipeline changes
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev dependencies
- **ai(rules[AGENTS])**: AI rule updates

Example:

```
Views(fix[DocutilsResponse]): Resolve rst_name from the template loader

why: A relative rst_name silently rendered nothing outside APP_DIRS.

what:
- Resolve rst_name through the configured template loader
- Add a regression test for a non-APP_DIRS TEMPLATES config
```

For a multi-line message, use a heredoc so the formatting survives:

```console
$ git commit -m "$(cat <<'EOF'
Scope(feat[detail]): Concise description

why: Explanation of the change.

what:
- First change
- Second change
EOF
)"
```

### Release commits

Never create tags. Never push tags. The owner handles tagging and tag
pushes, because a tag triggers the publish workflow.

A release commit subject is plain and short: `Tag v<version>`. The detailed
why and what go in the body. Do not use the `Scope(type[detail]):` format
for a release — it buries the lede.

## Slop prevention

Treat AI slop as review-hostile noise, not as proof that text or code is
wrong. The goal is to maximise information density.

- **AI signatures.** No "Generated by", no conversational filler, no
  unexplained emoji, no tool metadata.
- **Brittle references.** No hard-coded line numbers, fragile file counts,
  dated "as of" claims, bare SHAs, or local absolute paths — unless they are
  strict evidentiary artefacts, such as a benchmark log, a release note, a
  stack trace, or a lockfile entry, where the exact count, date, or SHA is
  the evidence.
- **Diff narration.** Do not restate what moved, was renamed, or was
  removed in anything the reader holds alongside the diff: code,
  docstrings, README, CHANGES, or a pull request description. The diff and
  the commit message already carry it.
- **Branch-internal narrative.** Do not mention intermediate states,
  abandoned approaches, or "no longer" behaviour unless users of the most
  recently published release actually experienced the old state — use
  trunk or the parent branch as the baseline when judging this, not an
  intermediate commit on the current branch.
- **Low-value scaffolding.** No ownerless TODOs, unused future-proofing,
  debug artefacts, or defensive wrappers around failure modes nothing can
  reach.
- **Prose inflation.** The diction table under [Voice](#voice) governs;
  replace an inflated word with a concrete description of behaviour,
  constraints, or trade-offs.
- **Coded labels.** Write rules and findings as plain imperatives. No
  `[R1]`, `Option B`, or any index a reader has to decode in shipped text.
  Internal agent bookkeeping may use ids; shipped text may not.

Preserve the "why". Never delete a comment documenting an invariant, a
protocol constraint, a platform quirk, or an upstream workaround — those are
the facts [Source comments](#source-comments) keeps, and every other comment
is judged by it.

### Durable source links

Link to a pinned revision, never to trunk, except for a living document —
this file, `AGENTS.md`, `.github/CONTRIBUTING.md` — meant to always show
current state, where `blob/master/…` is correct on purpose.

- Prefer a release tag: `blob/v0.31.1/…`. Most durable, and it tells the
  reader which released version the claim held for.
- Otherwise a 7-character commit SHA reachable from trunk:
  `blob/9a29b1a/…`. Never a pull-request-head SHA — it can be rebased or
  garbage-collected.
- Line anchors (`#L120-L145`) are only safe on a pinned ref.

### Cleaning up slop already committed

When removing slop from commits a branch already made, diff against the
parent branch first to scope what this branch actually introduced. Prefer
`fixup!` commits landed with `git rebase --autosquash` over a single
after-the-fact cleanup commit, and never rewrite a commit outside that
scope — especially a colleague's — without asking.
