"""Settings objects and type-mapping for Django Docutils library package."""
import typing as t

from django.conf import settings
from django.core.signals import setting_changed

if t.TYPE_CHECKING:
    from .types import DjangoDocutilsLibRSTSettings, DjangoDocutilsLibTextSettings

DJANGO_DOCUTILS_LIB_RST = t.cast(
    "DjangoDocutilsLibRSTSettings",
    getattr(settings, "DJANGO_DOCUTILS_LIB_RST", {}),
)
"""Settings for reStructuredText"""

DJANGO_DOCUTILS_LIB_TEXT = t.cast(
    "DjangoDocutilsLibTextSettings",
    getattr(settings, "DJANGO_DOCUTILS_LIB_TEXT", {"uncapitalized_word_filters": []}),
)

DJANGO_DOCUTILS_ANONYMOUS_USER_NAME: str | None = "AnonymousCoward"


def reload_settings(
    signal: t.Any,
    sender: t.Any,
    setting: str,
    value: t.Any,
    enter: bool,
    **kwargs: t.Any,
) -> None:
    """Ran when settings updated."""
    if setting == "DJANGO_DOCUTILS_LIB_RST" and isinstance(value, dict):
        # mypy: See mypy#6262, mypy#9168. There's no equivalent to keyof in TypeScript
        DJANGO_DOCUTILS_LIB_RST.update(**value)  # type:ignore

        # Register any added docutils roles or directives
        from django_docutils.lib.directives.registry import (
            register_django_docutils_directives,
        )
        from django_docutils.lib.roles.registry import register_django_docutils_roles

        register_django_docutils_roles()
        register_django_docutils_directives()


setting_changed.connect(reload_settings)
