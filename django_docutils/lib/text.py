import re

from django.conf import settings
from django.utils.module_loading import import_string

_word_re = re.compile(r'\w+', re.UNICODE)
_word_beginning_split_re = re.compile(r'([\s\(\{\[\<]+)', re.UNICODE)


def is_uncapitalized_word(value):
    """Return True if term/word segment is special uncap term (e.g. "django-")

    :param value: string value from template
    :type value: string

    Functions can be declared via BASED_TEXT in django settings via string
    imports. The filters accept one argument (the word). If you don't want the
    word/pattern capitalized, return True. Anything else capitalizes as normal.

    How to create filters:;

        def handle_uncapped_word(value):
            if value.startswith('django-'):
                return True
            if 'vs' in value:
                return True
            return False

    In your settings::

        BASED_LIB_TEXT = {
            'uncapitalized_word_filters': [
                'develtech.path.to.handle_uncapped_word'
            ]
        }
    """
    try:
        config = settings.BASED_LIB_TEXT
    except AttributeError:
        return

    if 'uncapitalized_word_filters' in config:
        for filter_fn_str in config['uncapitalized_word_filters']:
            filter_ = import_string(filter_fn_str)
            if filter_(value):
                return True
    return False


def smart_capfirst(value):
    """Capitalize the first character of the value."""

    if is_uncapitalized_word(value):
        return value

    return value[0].upper() + value[1:]


def smart_title(value):
    """Convert a string into titlecase, except for special cases.

    Django can still be capitalized, but it must already be like that.
    """

    return ''.join(
        [smart_capfirst(item) for item in _word_beginning_split_re.split(value) if item]
    )
