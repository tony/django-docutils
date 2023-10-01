import typing as t

import pytest
from django.template import Context, Template


def test_filter(settings: t.Any) -> None:
    template = Template(
        """{% load django_docutils %}
{% filter rst %}
hey
---

hi
##

A. hows
B. it

C. going
D. today

**hi**
*hi*
{% endfilter %}
"""
    )
    with pytest.warns(DeprecationWarning) as record:
        assert (
            template.render(Context({}))
            == r"""
<main id="hey">
<h1 class="title is-1">hey</h1>
<p class="subtitle" id="hi">hi</p>
<ol class="upperalpha simple">
<li><p>hows</p></li>
<li><p>it</p></li>
<li><p>going</p></li>
<li><p>today</p></li>
</ol>
<p><strong>hi</strong>
<em>hi</em></p>
</main>

"""
        )
        message = record[0].message
        assert isinstance(message, Warning)
        assert message.args[0] == "The rst filter has been deprecated"


def test_templatetag(settings: t.Any) -> None:
    content = """
hey
---

hi
##

A. hows
B. it

C. going
D. today

**hi**
*hi*
"""

    template = Template(
        """{% load django_docutils %}
{% rst content %}
"""
    )

    assert (
        template.render(Context({"content": content}))
        == """
<main id="hey">
<h1 class="title is-1">hey</h1>
<p class="subtitle" id="hi">hi</p>
<ol class="upperalpha simple">
<li><p>hows</p></li>
<li><p>it</p></li>
<li><p>going</p></li>
<li><p>today</p></li>
</ol>
<p><strong>hi</strong>
<em>hi</em></p>
</main>

"""
    )


def test_templatetag_show_title(settings: t.Any) -> None:
    content = """
hey
---

hi
##

A. hows
B. it

C. going
D. today

**hi**
*hi*
"""

    template = Template(
        """{% load django_docutils %}
{% rst content show_title=False %}
"""
    )

    assert (
        template.render(Context({"content": content}))
        == """
<ol class="upperalpha simple">
<li><p>hows</p></li>
<li><p>it</p></li>
<li><p>going</p></li>
<li><p>today</p></li>
</ol>
<p><strong>hi</strong>
<em>hi</em></p>

"""
    )


def test_templatetag_toc_only(settings: t.Any) -> None:
    content = """
hey
---

hi
##

My first section
----------------

Some text

My second section
-----------------

Additional text

A. hows
B. it

C. going
D. today

**hi**
*hi*
"""

    template = Template(
        """{% load django_docutils %}
{% rst content toc_only=True %}
"""
    )

    assert (
        template.render(Context({"content": content}))
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
    template = Template(
        """{% load django_docutils %}
{% rst toc_only=True %}
hey
---

hi
##

My first section
----------------

Some text

My second section
-----------------

Additional text

A. hows
B. it

C. going
D. today

**hi**
*hi*
{% endrst %}
"""
    )

    assert (
        template.render(Context({}))
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
    template = Template(
        """{% load django_docutils %}
{% rst %}
hey
---

hi
##

A. hows
B. it

C. going
D. today

**hi**
*hi2*
{% endrst %}"""
    )

    assert (
        template.render(Context({}))
        == r"""
<main id="hey">
<h1 class="title is-1">hey</h1>
<p class="subtitle" id="hi">hi</p>
<ol class="upperalpha simple">
<li><p>hows</p></li>
<li><p>it</p></li>
<li><p>going</p></li>
<li><p>today</p></li>
</ol>
<p><strong>hi</strong>
<em>hi2</em></p>
</main>
"""
    )
