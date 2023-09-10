# django-docutils &middot; [![Python Package](https://img.shields.io/pypi/v/django-docutils.svg)](https://pypi.org/project/django-docutils/) [![License](https://img.shields.io/github/license/tony/django-docutils.svg)](https://github.com/tony/django-docutils/blob/master/LICENSE)

django-docutils, docutils (reStructuredText) support for Django

## Quickstart

Install django-docutils:

```console
$ pip install django-docutils
```

## Template filter

If you want to use the template filter, add it to your `INSTALLED_APPS` in your settings file:

```python
INSTALLED_APPS = [ # ... your default apps,
    'django_docutils'
]
```

Then in your template:

```django
{% load django_docutils %}
{% filter restructuredtext %}
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

You can also use a class-based view to render restructuredtext.

If you want to use reStructuredText as a django template engine, `INSTALLED_APPS` _isn't_ required,
instead you add this to your `TEMPLATES` variable in your settings:

```python
TEMPLATES = [ # .. your default engines
{
    'NAME': 'docutils',
    'BACKEND': 'django_docutils.engines.Docutils',
    'DIRS': [],
    'APP_DIRS': True,
}]
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
DJANGO_DOCUTILS_LIB_RST = {  # Optional, automatically maps roles, directives and transformers
    'docutils': {
        'raw_enabled': True,
        'strip_comments': True,
        'initial_header_level': 2,
    },
    'roles': {
        'local': {
            'gh': 'django_docutils.lib.roles.github.github_role',
            'twitter': 'django_docutils.lib.roles.twitter.twitter_role',
            'email': 'django_docutils.lib.roles.email.email_role',
        }
    },
    'font_awesome': {  # Transformer to inject <em class="<class>"></em>
        'url_patterns': {
            r'.*github.com.*': 'fab fa-github',
            r'.*twitter.com.*': 'fab fa-twitter',
            r'.*amzn.to.*': 'fab fa-amazon',
            r'.*amazon.com.*': 'fab fa-amazon',
            r'.*news.ycombinator.com*': 'fab fa-hacker-news',
            r'.*leanpub.com.*': 'fab fa-leanpub',
            r'.*python.org.*': 'fab fa-python',
            r'.*pypi.org.*': 'fab fa-python',
            r'.*djangoproject.com.*': 'fab fa-python',
            r'.*wikipedia.org.*': 'fab fa-wikipedia',
            r'((rtfd|readthedocs).)*$': 'fab fa-books',
            r'^mailto:.*': 'fas fa-envelope',
            r'((?!mywebsite.com|localhost).)*$': 'fas fa-external-link',
        }
    },
}

DJANGO_DOCUTILS_LIB_TEXT = {  # Optional
    'uncapitalized_word_filters': ['project.my_module.my_capitalization_fn']
}
```

## More information

- Python 3.8+
- Django 3.1+

[![Docs](https://github.com/tony/django-docutils/workflows/docs/badge.svg)](https://github.com/tony/django-docutils/actions?query=workflow%3A%22Docs%22)
[![Build Status](https://github.com/tony/django-docutils/workflows/tests/badge.svg)](https://github.com/tony/django-docutils/actions?query=workflow%3A%22tests%22)
[![Code Coverage](https://codecov.io/gh/tony/django-docutils/branch/master/graph/badge.svg)](https://codecov.io/gh/tony/django-docutils)
