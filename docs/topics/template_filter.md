(template_filter)=

# Template filter

## Setup

:::{seealso}

{ref}`Quickstart <quickstart>`

:::

Make sure `django_docutils` is added your `INSTALLED_APPS` in your settings file:

```python
INSTALLED_APPS = [
    # ... your default apps,
    'django_docutils'
]
```

## Using the django filter

In your HTML template:

```django
{% load django_docutils %}
{% filter rst %}
# hey
# how's it going
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
