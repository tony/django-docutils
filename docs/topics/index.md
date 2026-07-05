(topics)=

# Topics

High-level guides covering django-docutils features, configuration, and common patterns.

::::{grid} 1 1 2 2
:gutter: 2 2 3 3

:::{grid-item-card} Template Tag
:link: template_tag
:link-type: doc
Render [reStructuredText] inside [Django] templates with the
{func}`~django_docutils.templatetags.django_docutils.rst` tag.
:::

:::{grid-item-card} Template Filter
:link: template_filter
:link-type: doc
Legacy coverage for the deprecated
{func}`~django_docutils.templatetags.django_docutils.rst_filter` filter.
:::

:::{grid-item-card} Class-based View
:link: class_based_view
:link-type: doc
Serve RST-backed pages with {class}`~django_docutils.views.DocutilsView`.
:::

:::{grid-item-card} Security
:link: security
:link-type: doc
Understand locked-down defaults and trusted-content opt-ins.
:::

:::{grid-item-card} What is docutils?
:link: what_is_docutils
:link-type: doc
Untangle [docutils], reStructuredText, [Sphinx], and [Markdown].
:::

:::{grid-item-card} FAQ
:link: faq
:link-type: doc
Common questions about reStructuredText and django-docutils.
:::

::::

[reStructuredText]: https://docutils.sourceforge.io/rst.html
[Django]: https://docs.djangoproject.com/
[docutils]: https://docutils.sourceforge.io/
[Sphinx]: https://www.sphinx-doc.org/
[Markdown]: https://www.markdownguide.org/

```{toctree}
:hidden:

template_tag
template_filter
class_based_view
security
what_is_docutils
faq
```
