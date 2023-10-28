"""Tests for rst template filter and tags."""
import typing as t

import pytest
from django.template import Context, Template

from .constants import (
    DEFAULT_EXPECTED,
    DEFAULT_EXPECTED_CONTENT,
    DEFAULT_RST,
    DEFAULT_RST_WITH_SECTIONS,
)


def test_filter(settings: t.Any) -> None:
    """Assert rst filter via block renders HTML."""
    template = Template(
        r"""{% load django_docutils %}
{% filter rst %}
{{DEFAULT_RST}}
{% endfilter %}
""".replace("{{DEFAULT_RST}}", DEFAULT_RST)
    )
    with pytest.warns(DeprecationWarning) as record:
        assert template.render(Context()) == DEFAULT_EXPECTED
        message = record[0].message
        assert isinstance(message, Warning)
        assert message.args[0] == "The rst filter has been deprecated"


def test_templatetag(settings: t.Any) -> None:
    """Asserts rst block via variable renders HTML content."""
    template = Template(
        """{% load django_docutils %}
{% rst content %}
"""
    )

    assert template.render(Context({"content": DEFAULT_RST})) == DEFAULT_EXPECTED


def test_templatetag_show_title(settings: t.Any) -> None:
    """Asserts rst template via variable that preserves title."""
    template = Template(
        """{% load django_docutils %}
{% rst content show_title=False %}
""".strip()
    )

    assert (
        template.render(Context({"content": DEFAULT_RST}))
        == "\n" + DEFAULT_EXPECTED_CONTENT + "\n"
    )


def test_templatetag_toc_only(settings: t.Any) -> None:
    """Asserts rst template via variable w/ toc_only=True renders table of contents."""
    template = Template(
        """{% load django_docutils %}
{% rst content toc_only=True %}
""".strip()
    )

    assert (
        template.render(Context({"content": DEFAULT_RST_WITH_SECTIONS}))
        == """
<main class="fixed-toc-menu menu">
<p class="menu-label">Contents</p>
<nav class="contents toc" role="doc-toc">
<ul class="menu-list simple">
<li><a class="reference internal" href="#hey" id="reference-1">hey</a>
<ul class="menu-list">
<li><a class="reference internal" href="#hi" id="reference-2">hi</a>
</li>
</ul>
</li>
<li><a class="reference internal" href="#my-first-section" id="reference-3">My first section</a>
</li>
<li><a class="reference internal" href="#my-second-section" id="reference-4">My second section</a>
</li>
</ul>
</nav>
</main>
"""  # noqa: E501
    )


def test_templatetag_toc_only_block(settings: t.Any) -> None:
    """Asserts rst template via block w/ toc_only=True renders table of contents."""
    template = Template(
        """{% load django_docutils %}
{% rst toc_only=True %}
{{DEFAULT_RST_WITH_SECTIONS}}
{% endrst %}
""".replace("{{DEFAULT_RST_WITH_SECTIONS}}", DEFAULT_RST_WITH_SECTIONS).strip()
    )

    assert (
        template.render(Context())
        == """
<main class="fixed-toc-menu menu">
<p class="menu-label">Contents</p>
<nav class="contents toc" role="doc-toc">
<ul class="menu-list simple">
<li><a class="reference internal" href="#hey" id="reference-1">hey</a>
<ul class="menu-list">
<li><a class="reference internal" href="#hi" id="reference-2">hi</a>
</li>
</ul>
</li>
<li><a class="reference internal" href="#my-first-section" id="reference-3">My first section</a>
</li>
<li><a class="reference internal" href="#my-second-section" id="reference-4">My second section</a>
</li>
</ul>
</nav>
</main>
"""  # noqa: E501
    )


def test_templatetag_block(settings: t.Any) -> None:
    """Asserts rst template block render HTML content."""
    template = Template(
        """{% load django_docutils %}
{% rst %}
{{DEFAULT_RST}}
{% endrst %}
""".replace("{{DEFAULT_RST}}", DEFAULT_RST)
    )

    assert template.render(Context()) == DEFAULT_EXPECTED
