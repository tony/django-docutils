import typing as t

from django.conf import settings

if t.TYPE_CHECKING:
    from .types import DjangoDocutilsLibRSTSettings, DjangoDocutilsLibTextSettings

DJANGO_DOCUTILS_LIB_RST = t.cast(
    "DjangoDocutilsLibRSTSettings", getattr(settings, "DJANGO_DOCUTILS_LIB_RST", {})
)
"""Settings for reStructuredText"""

INJECT_FONT_AWESOME: bool = (
    DJANGO_DOCUTILS_LIB_RST.get("font_awesome", {}).get("url_patterns") is not None
)

DJANGO_DOCUTILS_LIB_TEXT = t.cast(
    "DjangoDocutilsLibTextSettings",
    getattr(settings, "DJANGO_DOCUTILS_LIB_TEXT", {"uncapitalized_word_filters": []}),
)
