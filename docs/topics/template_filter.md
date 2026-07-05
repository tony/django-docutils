(template_filter)=

# Template filter

The {func}`~django_docutils.templatetags.django_docutils.rst_filter` filter is
deprecated. Keep it for existing templates that already use [Django]'s filter
syntax, but use {ref}`template_tag` for new template blocks.

:::{seealso}

{ref}`Quickstart <quickstart>`

:::

## Setup

Add `django_docutils` to `INSTALLED_APPS` in your settings file:

```python
INSTALLED_APPS = [
    # ... your default apps,
    'django_docutils'
]
```

## Render filtered content

:::{important}

The `rst` filter uses locked-down [docutils] defaults. See {ref}`security`
before rendering user-authored RST or enabling trusted-content overrides.

:::

[Django]: https://docs.djangoproject.com/
[reStructuredText]: https://docutils.sourceforge.io/rst.html
[docutils]: https://docutils.sourceforge.io/

In your HTML template:

```django
{% load django_docutils %}
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
```

Output:

```html
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
```

:::{admonition} Explore the API

- {func}`~django_docutils.templatetags.django_docutils.rst_filter`

:::
