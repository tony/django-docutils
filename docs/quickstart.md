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

- [pipx]\:

  ```console
  $ pipx install --suffix=@next 'django-docutils' --pip-args '\--pre' --force
  // Usage: django-docutils@next
  ```

- [uv]\:

  ```console
  $ uv add django-docutils --prerelease allow
  ```

- [uvx]\:

  ```console
  $ uvx --from 'django-docutils' --prerelease allow django-docutils
  ```

via trunk (can break easily):

- [pip]\:

  ```console
  $ pip install -e git+https://github.com/tony/django-docutils.git#egg=django-docutils
  ```

- [pipx]\:

  ```console
  $ pipx install --suffix=@master 'django-docutils @ git+https://github.com/tony/django-docutils.git@master' --force
  ```

- [uv]\:

  ```console
  $ uv tool install django-docutils --from git+https://github.com/tony/django-docutils.git
  ```

[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pypa.github.io/pipx/docs/
[PyPI]: https://pypi.org/
[uv]: https://docs.astral.sh/uv/
[uvx]: https://docs.astral.sh/uv/guides/tools/

## New to reStructuredText?

[reStructuredText] is the markup language; [docutils] is the library that
parses and renders it. The official [primer][rst-primer] and
[quick reference][rst-quickref] cover the syntax; {ref}`what-is-docutils`
maps the wider ecosystem (docutils, Sphinx, Markdown), and the {ref}`faq`
answers common questions.

[reStructuredText]: https://docutils.sourceforge.io/rst.html
[docutils]: https://docutils.sourceforge.io/
[rst-primer]: https://docutils.sourceforge.io/docs/user/rst/quickstart.html
[rst-quickref]: https://docutils.sourceforge.io/docs/user/rst/quickref.html

## Add the Django app

Next, add `django_docutils` to your `INSTALLED_APPS` in your settings file:

```python
INSTALLED_APPS = [
    # ... your default apps,
    'django_docutils'
]
```

## Next steps

Choose the entry point for your Django site:

1. {ref}`template_tag`
2. {ref}`template_filter`
3. {ref}`class_based_view`
4. {ref}`security`

The rendering defaults disable docutils features that are risky on the web;
if your site accepts user-authored markup, start with {ref}`security`.
