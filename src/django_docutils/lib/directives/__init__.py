"""Register Douctils directives for Django Docutils."""
from django.utils.module_loading import import_string
from docutils.parsers.rst import directives

from ..settings import DJANGO_DOCUTILS_LIB_RST


def register_django_docutils_directives() -> None:
    """Register all directives, exists to avoid race conditions.

    Sometimes stuff like publish_parts can be ran from command line functions
    tests. There's also ways we could avoid this by placing it in __init__
    of django_docutils.lib, but that's a bit implicit. Investigate that later.

    In order to make this work across django projects, let's use django
    settings to register to them.

    Why? Not all django projects want code highlighting (which requires
    pygments). Let's use a TEMPLATES-style django config:

    >>> DJANGO_DOCUTILS_LIB_RST = {
    ...    'directives': {  #: directive-name: Directive class (import string)
    ...        'code-block': 'django_docutils.lib.directives.pygments.CodeBlock'
    ...    }
    ... }
    """
    if not DJANGO_DOCUTILS_LIB_RST:
        return

    if "directives" in DJANGO_DOCUTILS_LIB_RST:
        for dir_name, dir_cls_str in DJANGO_DOCUTILS_LIB_RST["directives"].items():
            class_ = import_string(dir_cls_str)
            directives.register_directive(dir_name, class_)
