|pypi| |docs| |build-status| |coverage| |license|

django-docutils, docutils (reStructuredText) support for Django

Documentation
-------------

The full documentation is at https://django-docutils.git-pull.com.

Quickstart
----------

Install django-docutils:

.. code-block:: sh

    pip install django-docutils

Template filter
---------------

If you want to use the template filter, add it to your ``INSTALLED_APPS``
in your settings file:

.. code-block:: python

    INSTALLED_APPS = [ # ... your default apps,
        'django_docutils'
    ]

Then in your template:

.. code-block:: django

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


Template engine (class-based view)
----------------------------------

You can also use a class-based view to render restructuredtext.

If you want to use reStructuredText as a django template engine,
``INSTALLED_APPS`` *isn't* required, instead you add this to your
``TEMPLATES`` variable in your settings:

.. code-block:: python

    TEMPLATES = [ # .. your default engines
    {
        'NAME': 'docutils',
        'BACKEND': 'django_docutils.engines.Docutils',
        'DIRS': [],
        'APP_DIRS': True,
    }]

Now django will be able to scan for .rst files and process them. In your
view:

.. code-block:: python

   from django_docutils.views import DocutilsView

   class HomeView(DocutilsView):
       template_name = 'base.html'
       rst_name = 'home.rst'

.. |pypi| image:: https://img.shields.io/pypi/v/django-docutils.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/django-docutils

.. |build-status| image:: https://img.shields.io/travis/tony/django-docutils.svg
   :alt: Build Status
   :target: https://travis-ci.org/tony/django-docutils

.. |coverage| image:: https://codecov.io/gh/tony/django-docutils/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/tony/django-docutils

.. |license| image:: https://img.shields.io/github/license/tony/django-docutils.svg
    :alt: License 

.. |docs| image:: https://readthedocs.org/projects/django-docutils/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.org/projects/django-docutils/
