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

New versions of django-docutils are published to PyPI as alpha, beta, or release candidates. In
their versions you will see notification like `a1`, `b1`, and `rc1`, respectively. `1.10.0b4` would
mean the 4th beta release of `1.10.0` before general availability.

- [pip]\:

  ```console
  $ pip install --upgrade --pre django-docutils
  ```

via trunk (can break easily):

- [pip]\:

  ```console
  $ pip install -e git+https://github.com/tony/django-docutils.git#egg=django-docutils
  ```

[pip]: https://pip.pypa.io/en/stable/

## Usage

```python
import django_docutils
```

See {ref}`Home page <index>`.
