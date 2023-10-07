(django_view)=

## Django view

Template engine (class-based view)

:::{seealso}

{ref}`Quickstart <quickstart>`.

:::

You can also use a class-based view to render reStructuredText (reST).

If you want to use reStructuredText as a django template engine, `INSTALLED_APPS` _isn't_ required,
instead you add this to your `TEMPLATES` variable in your settings:

```python
TEMPLATES = [
    # ... Other engines
    {
        "NAME": "docutils",
        "BACKEND": "django_docutils.engines.Docutils",
        "DIRS": [],
        "APP_DIRS": True,
    }
]
```

Now django will be able to scan for .rst files and process them. In your view:

```python
from django_docutils.views import DocutilsView

class HomeView(DocutilsView):
    template_name = 'base.html'
    rst_name = 'home.rst'
```
