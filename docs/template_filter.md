(template_filter)=

# Template filter

:::{seealso}

{ref}`Quickstart <quickstart>`.

:::

In your template:

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
