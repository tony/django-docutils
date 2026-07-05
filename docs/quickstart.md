(quickstart)=

# Quickstart

## Installation

Install the latest official version:

```console
$ pip install django-docutils
```

Upgrading:

```console
$ pip install --upgrade django-docutils
```

(developmental-releases)=

### Developmental releases

New versions of django-docutils are published to [PyPI] as alpha, beta, or
release candidates. Their versions use markers like `a1`, `b1`, and `rc1`,
respectively. `1.10.0b4` would mean the 4th beta release of `1.10.0` before
general availability.

- [pip]\:

  ```console
  $ pip install --upgrade --pre django-docutils
  ```

- [uv]\:

  ```console
  $ uv add django-docutils --prerelease allow
  ```

via trunk (can break easily):

- [pip]\:

  ```console
  $ pip install -e git+https://github.com/tony/django-docutils.git#egg=django-docutils
  ```

- [uv]\:

  ```console
  $ uv add "django-docutils @ git+https://github.com/tony/django-docutils.git"
  ```

[pip]: https://pip.pypa.io/en/stable/
[PyPI]: https://pypi.org/
[uv]: https://docs.astral.sh/uv/

## New to reStructuredText?

[reStructuredText] is the markup language; [docutils] is the library that
parses and renders it. The official [primer][rst-primer] and
[quick reference][rst-quickref] cover the syntax; {ref}`what-is-docutils`
maps the wider ecosystem (docutils, [Sphinx], [Markdown]), and the
{ref}`faq` answers common questions.

[reStructuredText]: https://docutils.sourceforge.io/rst.html
[docutils]: https://docutils.sourceforge.io/
[Sphinx]: https://www.sphinx-doc.org/
[Markdown]: https://www.markdownguide.org/
[rst-primer]: https://docutils.sourceforge.io/docs/user/rst/quickstart.html
[rst-quickref]: https://docutils.sourceforge.io/docs/user/rst/quickref.html

## Add the Django app

Next, add `django_docutils` to your `INSTALLED_APPS` in your [Django] settings
file:

```python
INSTALLED_APPS = [
    # ... your default apps,
    'django_docutils'
]
```

## Render your first block

Load the template tags and put a small reStructuredText document inside
`{% rst %}`:

```django
{% load django_docutils %}
{% rst %}
Hello
=====

Welcome to **reStructuredText** in Django.
{% endrst %}
```

Output:

```html
<main id="hello">
<h1 class="title is-1">Hello</h1>
<p>Welcome to <strong>reStructuredText</strong> in Django.</p>
</main>
```

## Next steps

Choose the entry point for your Django site:

1. {ref}`template_tag`
2. {ref}`class_based_view`
3. {ref}`security`
4. {ref}`template_filter` for legacy templates that already use the deprecated
   filter

The rendering defaults disable docutils features that are risky on the web;
if your site accepts user-authored markup, start with {ref}`security`.

[Django]: https://docs.djangoproject.com/
