"""Text related utilities for Django Docutils."""
import re

from django.conf import settings
from django.utils.module_loading import import_string

_word_re = re.compile(r"\w+", re.UNICODE)
_word_beginning_split_re = re.compile(r"([\s\(\{\[\<]+)", re.UNICODE)


def is_uncapitalized_word(value: str) -> bool:
    """Return True if term/word segment is special uncap term (e.g. "django-").

    Parameters
    ----------
    value : str
        string value from template

    Returns
    -------
    bool
        True if term or word is uncapitalized.

    Functions can be declared via DJANGO_DOCUTILS_TEXT in django settings via string
    imports. The filters accept one argument (the word). If you don't want the
    word/pattern capitalized, return True. Anything else capitalizes as normal.

    How to create filters:

    .. code-block:: python

       def handle_uncapped_word(value: str) -> bool:
           if value.startswith('django-'):
               return True
           if 'vs' in value:
               return True
           return False

    In your settings:

    .. code-block:: python

       DJANGO_DOCUTILS_LIB_TEXT = {
           'uncapitalized_word_filters': [
               'project.path.to.handle_uncapped_word'
           ]
       }
    """
    try:
        config = settings.DJANGO_DOCUTILS_LIB_TEXT
    except AttributeError:
        return False

    if "uncapitalized_word_filters" in config:
        for filter_fn_str in config["uncapitalized_word_filters"]:
            filter_ = import_string(filter_fn_str)
            if filter_(value):
                return True
    return False


def smart_capfirst(value: str) -> str:
    """Capitalize the first character of the value."""
    return value[0].upper() + value[1:]


def smart_title(value: str) -> str:
    """Convert a string into titlecase, except for special cases.

    Django can still be capitalized, but it must already be like that.
    """
    return "".join(
        [smart_capfirst(item) for item in _word_beginning_split_re.split(value) if item]
    )
