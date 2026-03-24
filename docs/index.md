(index)=

# django-docutils

Docutils (reStructuredText) support for Django templates, views, and template engines.

::::{grid} 1 1 2 2
:gutter: 2 2 3 3

:::{grid-item-card} Quickstart
:link: quickstart
:link-type: doc
Install and render your first RST snippet in 5 minutes.
:::

:::{grid-item-card} Topics
:link: topics/index
:link-type: doc
Template tags, template filters, class-based views, and FAQ.
:::

:::{grid-item-card} API Reference
:link: api/index
:link-type: doc
Every public class, function, and exception.
:::

:::{grid-item-card} Contributing
:link: project/index
:link-type: doc
Development setup, code style, release process.
:::

::::

## Install

```console
$ pip install django-docutils
```

```console
$ uv add django-docutils
```

See [Quickstart](quickstart.md) for configuration and first steps.

## At a glance

```django
{% load django_docutils %}

{% rst %}
Title
=====

*reStructuredText* rendered to HTML inside a Django template.
{% endrst %}
```

```{toctree}
:hidden:

quickstart
topics/index
api/index
project/index
history
GitHub <https://github.com/tony/django-docutils>
```
