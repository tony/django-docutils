(api)=

# API Reference

:::{seealso}

{ref}`Quickstart <quickstart>`.

:::

::::{grid} 1 1 2 2
:gutter: 2 2 3 3

:::{grid-item-card} Exceptions
:link: exc
:link-type: doc
Exception definitions for django-docutils.
:::

:::{grid-item-card} Views
:link: views
:link-type: doc
{class}`~django_docutils.views.DocutilsView` and
{class}`~django_docutils.views.DocutilsResponse`.
:::

:::{grid-item-card} Lib
:link: lib/index
:link-type: doc
Publisher, roles, directives, writers, and transforms.
:::

:::{grid-item-card} Template Engine
:link: template
:link-type: doc
{class}`~django_docutils.template.DocutilsTemplates` backend for [Django].
:::

:::{grid-item-card} Template Tags
:link: templatetags/index
:link-type: doc
{func}`~django_docutils.templatetags.django_docutils.rst` tag and
{func}`~django_docutils.templatetags.django_docutils.rst_filter` internals.
:::

::::

```{toctree}
:maxdepth: 1
:hidden:

exc
views
lib/index
template
templatetags/index
```

[Django]: https://docs.djangoproject.com/
