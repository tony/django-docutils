(api)=

# API Reference

:::{seealso}

{ref}`Quickstart <quickstart>`.

:::

## Inside

```{toctree}
:maxdepth: 1

directives
engines
exc
models
views


lib/index
pygments/index
templatetags/index
```

## Common

### Directives

```{eval-rst}
.. autofunction:: django_docutils.directives.register_pygments_directive
```

```{eval-rst}
.. autodata:: django_docutils.directives.DEFAULT
```

```{eval-rst}
.. autodata:: django_docutils.directives.VARIANTS
```

### Code block

```{eval-rst}
.. autoclass:: django_docutils.directives.CodeBlock
   :members:
   :inherited-members:
   :private-members:
   :show-inheritance:
   :member-order: bysource
```

### Exceptions

```{eval-rst}
.. autoexception:: django_docutils.exc.DjangoDocutilsException
```
