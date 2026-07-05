(class_based_view)=

# Class-based view

Use {class}`~django_docutils.views.DocutilsView` when a [reStructuredText] file
should behave like a [Django] view page. Django chooses the outer template,
django-docutils renders the `.rst` source, and the view passes the rendered
HTML as `content`.

For applications that want Django to load `.rst` files through a template
backend, {class}`~django_docutils.template.DocutilsTemplates` provides the
[docutils] engine.

:::{seealso}

{ref}`Quickstart <quickstart>`
:::

:::{important}

Both entry points use locked-down docutils defaults. See {ref}`security` before
serving user-authored RST or enabling trusted-content overrides.

:::

[reStructuredText]: https://docutils.sourceforge.io/rst.html
[Django]: https://docs.djangoproject.com/
[docutils]: https://docutils.sourceforge.io/

## Setup

You do not need `INSTALLED_APPS` for the backend-only path. Add the docutils
backend to `TEMPLATES` instead:

```python
TEMPLATES = [
    # ... Other engines
    {
        "NAME": "docutils",
        "BACKEND": "django_docutils.template.DocutilsTemplates",
        "DIRS": [],
        "APP_DIRS": True,
    }
]
```

## Render a view

With the backend configured, your view points at an RST template:

```python
from django_docutils.views import DocutilsView

class HomeView(DocutilsView):
    template_name = 'base.html'
    rst_name = 'home.rst'
```

*yourapp/templates/home.rst*:

````restructuredtext
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
````

*yourapp/templates/base.html*:

```django
{{content}}
```

Output:

```html
<div class="document" id="hey">
<h1 class="title">hey</h1>
<h2 class="subtitle" id="hi">hi</h2>
<ol class="upperalpha simple">
<li>hows</li>
<li>it</li>
<li>going</li>
<li>today</li>
</ol>
<p><strong>hi</strong>
<em>hi</em></p>
</div>
```

:::{admonition} Explore the API

- {class}`~django_docutils.views.DocutilsView`, {class}`~django_docutils.views.DocutilsResponse`
- {class}`~django_docutils.lib.views.RSTMixin`,
  {class}`~django_docutils.lib.views.RSTRawView`, {class}`~django_docutils.lib.views.RSTView`
- {class}`~django_docutils.template.DocutilsTemplates`, {class}`~django_docutils.template.DocutilsTemplate`

:::
