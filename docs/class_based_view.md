(class_based_view)=

# Class-based view

## Setup

:::{seealso}

{ref}`Quickstart <quickstart>`
:::

You can also use a class-based view to render reStructuredText (reST).

If you want to use reStructuredText as a django template engine, `INSTALLED_APPS` _isn't_ required,
instead you add this to your `TEMPLATES` variable in your settings:

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

## Introduction to views

Now django will be able to scan for .rst files and process them. In your view:

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
