"""Register douctils directives for django-docutils."""
from django.utils.module_loading import import_string
from docutils.parsers.rst import directives

from ..settings import DJANGO_DOCUTILS_LIB_RST


def register_django_docutils_directives() -> None:
    """Register docutils directives for a django application.

    Examples
    --------
    In your site's :ref:`Django settings module<django:django-settings-module>`:

    >>> DJANGO_DOCUTILS_LIB_RST = {
    ...    'directives': {  #: directive-name: Directive class (import string)
    ...        'code-block': 'django_docutils.lib.directives.code.CodeBlock'
    ...    }
    ... }
    """
    if not DJANGO_DOCUTILS_LIB_RST:
        return

    if "directives" in DJANGO_DOCUTILS_LIB_RST:
        for dir_name, dir_cls_str in DJANGO_DOCUTILS_LIB_RST["directives"].items():
            class_ = import_string(dir_cls_str)
            directives.register_directive(dir_name, class_)
