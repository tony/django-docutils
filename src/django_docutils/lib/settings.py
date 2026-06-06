"""Settings objects and type-mapping for Django Docutils library package."""

from __future__ import annotations

import typing as t

from django.conf import settings
from django.core.signals import setting_changed

if t.TYPE_CHECKING:
    from .types import DjangoDocutilsLibRSTSettings, DjangoDocutilsLibTextSettings

SAFE_DOCUTILS_DEFAULTS: t.Final[dict[str, object]] = {
    "file_insertion_enabled": False,
    "raw_enabled": False,
    "_disable_config": True,
    "line_length_limit": 10_000,
}
"""Docutils defaults used for web-facing django-docutils rendering."""

PROTECTED_DOCUTILS_DEFAULTS: t.Final[dict[str, object]] = {
    "file_insertion_enabled": False,
    "raw_enabled": False,
    "_disable_config": True,
}
"""Settings that require explicit unsafe opt-in before applications may override."""

DEFAULT_ALLOWED_URI_SCHEMES: t.Final[frozenset[str]] = frozenset(
    {"http", "https", "mailto"},
)
"""URI schemes emitted by django-docutils HTML rendering by default."""

UNSAFE_URI_SCHEMES: t.Final[frozenset[str]] = frozenset(
    {"data", "file", "javascript", "vbscript"},
)
"""URI schemes that require explicit unsafe opt-in when configured."""

# Copy so the module state never aliases Django's stored settings object;
# reload_settings() mutates this dict in place on setting_changed.
DJANGO_DOCUTILS_LIB_RST = t.cast(
    "DjangoDocutilsLibRSTSettings",
    dict(getattr(settings, "DJANGO_DOCUTILS_LIB_RST", {})),
)
"""Settings for reStructuredText"""

DJANGO_DOCUTILS_LIB_TEXT = t.cast(
    "DjangoDocutilsLibTextSettings",
    getattr(settings, "DJANGO_DOCUTILS_LIB_TEXT", {"uncapitalized_word_filters": []}),
)

DJANGO_DOCUTILS_ANONYMOUS_USER_NAME: str | None = "AnonymousCoward"


def unsafe_docutils_settings_allowed() -> bool:
    """Return whether project settings may re-enable unsafe Docutils features.

    Examples
    --------
    >>> isinstance(unsafe_docutils_settings_allowed(), bool)
    True
    """
    return bool(DJANGO_DOCUTILS_LIB_RST.get("allow_unsafe_docutils_settings", False))


def get_docutils_settings(
    settings_overrides: t.Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Return Docutils settings with django-docutils security defaults applied.

    Examples
    --------
    >>> settings = get_docutils_settings()
    >>> settings["file_insertion_enabled"]
    False
    >>> settings["raw_enabled"]
    False
    >>> settings["_disable_config"]
    True
    """
    configured = dict(DJANGO_DOCUTILS_LIB_RST.get("docutils", {}))
    overrides = dict(settings_overrides or {})
    resolved: dict[str, object] = {
        **SAFE_DOCUTILS_DEFAULTS,
        **configured,
        **overrides,
    }

    if not unsafe_docutils_settings_allowed():
        resolved.update(PROTECTED_DOCUTILS_DEFAULTS)
        line_length_limit = resolved.get("line_length_limit")
        if isinstance(line_length_limit, int) and line_length_limit > 10_000:
            resolved["line_length_limit"] = 10_000

    return resolved


def get_allowed_uri_schemes() -> frozenset[str]:
    """Return normalized URI schemes allowed in rendered HTML attributes.

    Examples
    --------
    >>> "https" in get_allowed_uri_schemes()
    True
    >>> "javascript" in get_allowed_uri_schemes()
    False
    """
    configured = DJANGO_DOCUTILS_LIB_RST.get(
        "allowed_uri_schemes",
        DEFAULT_ALLOWED_URI_SCHEMES,
    )
    schemes = {str(scheme).lower().removesuffix(":") for scheme in configured}
    if not unsafe_docutils_settings_allowed():
        schemes -= UNSAFE_URI_SCHEMES
    return frozenset(schemes)


def reload_settings(
    signal: t.Any,
    sender: t.Any,
    setting: str,
    value: t.Any,
    enter: bool,
    **kwargs: t.Any,
) -> None:
    """Ran when settings updated.

    Examples
    --------
    >>> before = dict(DJANGO_DOCUTILS_LIB_RST)
    >>> reload_settings(None, None, "DJANGO_DOCUTILS_LIB_RST", {"transforms": []}, True)
    >>> DJANGO_DOCUTILS_LIB_RST["transforms"]
    []
    >>> reload_settings(None, None, "DJANGO_DOCUTILS_LIB_RST", dict(before), False)
    >>> dict(DJANGO_DOCUTILS_LIB_RST) == before
    True
    """
    if setting == "DJANGO_DOCUTILS_LIB_RST" and isinstance(value, dict):
        # Snapshot before clear(): on override_settings teardown, value can be
        # the same object as DJANGO_DOCUTILS_LIB_RST.
        new_value = dict(value)
        # mypy: See mypy#6262, mypy#9168. There's no equivalent to keyof in TypeScript
        rst_settings = t.cast("t.MutableMapping[str, object]", DJANGO_DOCUTILS_LIB_RST)
        rst_settings.clear()
        rst_settings.update(new_value)

        # Register any added docutils roles or directives
        from django_docutils.lib.directives.registry import (
            register_django_docutils_directives,
        )
        from django_docutils.lib.roles.registry import register_django_docutils_roles

        register_django_docutils_roles()
        register_django_docutils_directives()


setting_changed.connect(reload_settings)
