# django-docutils &middot; [![Python Package](https://img.shields.io/pypi/v/django-docutils.svg)](https://pypi.org/project/django-docutils/0.5.1/) [![License](https://img.shields.io/github/license/tony/django-docutils.svg)](https://github.com/tony/django-docutils/blob/master/LICENSE)

django-docutils, docutils (reStructuredText) support for Django

## Quickstart

Install django-docutils:

```console
$ pip install django-docutils
```

Favicons:

```console
$ pip install django-docutils[favicon]
```

intersphinx support:

```console
$ pip install django-docutils[intersphinx]
```

Both:

```console
$ pip install django-docutils[favicon,intersphinx]
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
BASED_LIB_RST = {  # Optional, automatically maps roles, directives and transformers
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

BASED_LIB_TEXT = {  # Optional
    'uncapitalized_word_filters': ['project.my_module.my_capitalization_fn']
}

BASED_ADS = {  # If injecting ads
    'AMAZON_AD_CODE': """
    <script type="text/javascript">
    amzn_assoc_placement = "adunit0";
    amzn_assoc_search_bar = "true";
    amzn_assoc_tracking_id = "mytracking-20";
    amzn_assoc_search_bar_position = "bottom";
    amzn_assoc_ad_mode = "search";
    amzn_assoc_ad_type = "smart";
    amzn_assoc_marketplace = "amazon";
    amzn_assoc_region = "US";
    amzn_assoc_title = "You may be interested in";
    amzn_assoc_default_search_phrase = "{keyword}";
    amzn_assoc_default_category = "All";
    amzn_assoc_linkid = "6efef5538142e4a4031b04de66b6e804";
    </script>
    <script src="//z-na.amazon-adsystem.com/widgets/onejs?MarketPlace=US"></script>
    """,
    'AMAZON_AD_STRIP': (
        '<script src="//z-na.amazon-adsystem.com/widgets/onejs?MarketPlace=US&'
        'adInstanceId=521gc14d-d9f1-4691-8af2-a38de0d0cbad"></script>'
    ),
    'GOOGLE_AD_CODE': """
    <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js">
    </script>
    <ins class="adsbygoogle"
         style="display:block; text-align:center;"
         data-ad-layout="in-article"
         data-ad-format="fluid"
         data-ad-client="ca-pub-5555555555555555"
         data-ad-slot="5555555555"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
    """,
}
```

## More information

- Python 3.8+
- Django 3.0+

[![Docs](https://github.com/tony/django-docutils/workflows/docs/badge.svg)](https://github.com/tony/django-docutils/actions?query=workflow%3A%22Docs%22)
[![Build Status](https://github.com/tony/django-docutils/workflows/tests/badge.svg)](https://github.com/tony/django-docutils/actions?query=workflow%3A%22tests%22)
[![Code Coverage](https://codecov.io/gh/tony/django-docutils/branch/master/graph/badge.svg)](https://codecov.io/gh/tony/django-docutils)
