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

:::{admonition} Explore the API

- {func}`~django_docutils.templatetags.django_docutils.rst_filter`

:::
