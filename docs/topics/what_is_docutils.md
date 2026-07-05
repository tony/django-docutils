(what-is-docutils)=

# What is docutils?

A field guide to the names you will meet when rendering markup in [Django]:
[docutils], [reStructuredText], [Sphinx], and friends — and where
django-docutils fits among them.

## What is reStructuredText?

[reStructuredText] (also written *reST*, *RST*, or *rst*) is a plaintext
markup language, comparable to [Markdown] but older and more extensible. The
fastest ways in are the official [primer][rst-primer] and the
[quick reference][rst-quickref].

## What is docutils?

[docutils] is the Python library that parses reStructuredText and publishes it
to other formats. reStructuredText is the language; docutils is the processing
system — the parser is one docutils component, the output writers are others.
The [docutils documentation][docutils-docs] covers both halves.

## What is Sphinx — and is django-docutils Sphinx?

[Sphinx] is a documentation generator built on top of docutils: it adds
cross-references, multi-page projects, themes, and extensions, and it renders
sites like the [Python documentation](https://docs.python.org/). Its
[reStructuredText primer][sphinx-primer] is another good introduction.

django-docutils is not Sphinx. It renders RST fragments and pages inside
Django templates and views:

| Tool            | Built on          | Use it for                              |
| --------------- | ----------------- | --------------------------------------- |
| [docutils]      | —                 | Parsing and rendering single documents  |
| [Sphinx]        | docutils          | Documentation sites and books           |
| [MyST-Parser]   | docutils / Sphinx | Markdown in docutils and Sphinx         |
| django-docutils | docutils + Django | RST inside Django templates and views   |

## Can docutils parse Markdown?

Yes — since docutils 0.19, with a third-party parser installed:
[myst-docutils] (recommended) or [pycmark]. docutils selects them through its
`markdown` / `commonmark` parser aliases — see the
[docutils configuration reference][docutils-config]. The older
[recommonmark](https://pypi.org/project/recommonmark/) wrapper is deprecated
and will be removed in docutils 1.0.

django-docutils itself renders reStructuredText. To serve
[CommonMark](https://commonmark.org/) Markdown in a docutils or Sphinx
pipeline, reach for [MyST-Parser].

## What can docutils output?

reStructuredText input can leave docutils in many formats — django-docutils
uses the HTML writer family, the rest come with the
[docutils CLI tools][docutils-tools] such as `rst2html5`, `rst2latex`, and
`rst2man`:

| Writer                       | Output                                  |
| ---------------------------- | --------------------------------------- |
| `html5`                      | HTML5                                   |
| `html4css1`                  | XHTML 1.0 (the `html` default for now)  |
| `latex2e`, `xetex`           | LaTeX / XeTeX, typically en route to PDF |
| `manpage`                    | Unix man pages                          |
| `odf_odt`                    | OpenDocument text (LibreOffice)         |
| `s5_html`                    | S5 HTML slideshows                      |
| `docutils_xml`, `pseudoxml`  | Document-tree XML / debugging output    |

## Where does django-docutils fit?

Your template or view hands RST source to django-docutils — via
{ref}`template_tag`, {ref}`template_filter`, or {ref}`class_based_view` —
which runs the docutils parser with hardened settings, removes raw nodes and
unsafe link targets from the document tree, and returns HTML produced by
docutils' HTML writers.

Rendering user-authored markup carries risk that configuration can reduce,
not remove — see {ref}`security` and docutils' own
[security guide][docutils-security].

[docutils]: https://docutils.sourceforge.io/
[Django]: https://docs.djangoproject.com/
[docutils-docs]: https://docutils.sourceforge.io/docs/
[docutils-config]: https://docutils.sourceforge.io/docs/user/config.html
[docutils-tools]: https://docutils.sourceforge.io/docs/user/tools.html
[docutils-security]: https://docutils.sourceforge.io/docs/howto/security.html
[reStructuredText]: https://docutils.sourceforge.io/rst.html
[rst-primer]: https://docutils.sourceforge.io/docs/user/rst/quickstart.html
[rst-quickref]: https://docutils.sourceforge.io/docs/user/rst/quickref.html
[Sphinx]: https://www.sphinx-doc.org/
[sphinx-primer]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
[Markdown]: https://www.markdownguide.org/
[MyST-Parser]: https://myst-parser.readthedocs.io/
[myst-docutils]: https://pypi.org/project/myst-docutils/
[pycmark]: https://pypi.org/project/pycmark/
