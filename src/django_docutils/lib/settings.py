"""Settings objects and type-mapping for Django Docutils library package."""
import typing as t

from django.conf import settings

if t.TYPE_CHECKING:
    from .types import DjangoDocutilsLibRSTSettings, DjangoDocutilsLibTextSettings

DJANGO_DOCUTILS_LIB_RST = t.cast(
    "DjangoDocutilsLibRSTSettings", getattr(settings, "DJANGO_DOCUTILS_LIB_RST", {})
)
"""Settings for reStructuredText"""

DJANGO_DOCUTILS_LIB_TEXT = t.cast(
    "DjangoDocutilsLibTextSettings",
    getattr(settings, "DJANGO_DOCUTILS_LIB_TEXT", {"uncapitalized_word_filters": []}),
)

DJANGO_DOCUTILS_ANONYMOUS_USER_NAME: str | None = "AnonymousCoward"
