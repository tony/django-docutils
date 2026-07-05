(template_tag)=

# Template tag

Use {func}`~django_docutils.templatetags.django_docutils.rst` when the RST
source lives directly in a Django template block. The tag sends that block to
the django-docutils publisher and returns HTML for Django to insert into the
page.

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

## Render a template block

:::{important}

The `{% rst %}` tag uses locked-down Docutils defaults. See {ref}`security`
before rendering user-authored RST or enabling trusted-content overrides.

:::

In your HTML template:

```django
{% load django_docutils %}
{% rst %}
# hey
# how's it going
A. hows
B. it

C. going
D. today

**hi**
*hi*
{% endrst %}
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

- {func}`~django_docutils.templatetags.django_docutils.rst`

:::
