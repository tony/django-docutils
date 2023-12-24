# django-docutils &middot; [![Python Package](https://img.shields.io/pypi/v/django-docutils.svg)](https://pypi.org/project/django-docutils/) [![License](https://img.shields.io/github/license/tony/django-docutils.svg)](https://github.com/tony/django-docutils/blob/master/LICENSE)

docutils (a.k.a. reStructuredText / rst / reST) support for Django.

## Quickstart

Install django-docutils:

```console
$ pip install django-docutils
```

Next, add `django_docutils` to your `INSTALLED_APPS` in your settings file:

```python
INSTALLED_APPS = [
    # ... your default apps,
    'django_docutils'
]
```

## Template tag

In your template:

```django
{% load django_docutils %}
{% rst %}
# hey
# how's it going
A. hows
B. it

C. going
D. today

**hi**
*hi*
{% endrst %}
```

## Template filter

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

## Template engine (class-based view)

You can also use a class-based view to render reStructuredText (reST).

If you want to use reStructuredText as a django template engine, `INSTALLED_APPS` _isn't_ required,
instead you add this to your `TEMPLATES` variable in your settings:

```python
TEMPLATES = [
    # ... Other engines
    {
        "NAME": "docutils",
        "BACKEND": "django_docutils.template.DocutilsTemplates",
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

# Settings

```python
# Optional, automatically maps roles, directives and transformers
DJANGO_DOCUTILS_LIB_RST = {
    "docutils": {
        "raw_enabled": True,
        "strip_comments": True,
        "initial_header_level": 2,
    },
    "roles": {
        "local": {
            "gh": "django_docutils.lib.roles.github.github_role",
            "twitter": "django_docutils.lib.roles.twitter.twitter_role",
            "email": "django_docutils.lib.roles.email.email_role",
        }
    },
    "directives": {
        "code-block": "django_docutils.lib.directives.code.CodeBlock",
    }
}

# Optional
DJANGO_DOCUTILS_LIB_TEXT = {
    "uncapitalized_word_filters": ["project.my_module.my_capitalization_fn"]
}
```

## More information

- Python 3.8+
- Django 3.2+

[![Docs](https://github.com/tony/django-docutils/workflows/docs/badge.svg)](https://github.com/tony/django-docutils/actions?query=workflow%3A%22Docs%22)
[![Build Status](https://github.com/tony/django-docutils/workflows/tests/badge.svg)](https://github.com/tony/django-docutils/actions?query=workflow%3A%22tests%22)
[![Code Coverage](https://codecov.io/gh/tony/django-docutils/branch/master/graph/badge.svg)](https://codecov.io/gh/tony/django-docutils)
