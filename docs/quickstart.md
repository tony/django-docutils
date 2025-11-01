(quickstart)=

# Quickstart

## Installation

For latest official version:

```console
$ pip install django-docutils
```

Upgrading:

```console
$ pip install --upgrade django-docutils
```

(developmental-releases)=

### Developmental releases

New versions of django-docutils are published to PyPI as alpha, beta, or release candidates.
In their versions you will see notification like `a1`, `b1`, and `rc1`, respectively.
`1.10.0b4` would mean the 4th beta release of `1.10.0` before general availability.

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
[uv]: https://docs.astral.sh/uv/
[uvx]: https://docs.astral.sh/uv/guides/tools/

## Add the django app

Next, add `django_docutils` to your `INSTALLED_APPS` in your settings file:

```python
INSTALLED_APPS = [
    # ... your default apps,
    'django_docutils'
]
```

## Next steps

Integate docutils to your django site:

1. {ref}`template_tag`
2. {ref}`template_filter`
3. {ref}`class_based_view`

:::
