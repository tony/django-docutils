"""Typings for Django Docutils settings for django."""

from __future__ import annotations

from typing import TypedDict


class DjangoDocutilsLibRSTRolesSettings(TypedDict, total=False):
    """Docutils role mappings."""

    local: dict[str, str]


class DjangoDocutilsLibRSTDocutilsSettings(TypedDict, total=False):
    """Docutils document settings."""

    raw_enabled: bool
    strip_comments: bool
    initial_header_level: int


class DjangoDocutilsLibRSTSettings(TypedDict, total=False):
    """Core settings object for ``DJANGO_DOCUTILS_LIB_RST``."""

    metadata_processors: list[str]
    transforms: list[str]
    docutils: DjangoDocutilsLibRSTDocutilsSettings
    directives: dict[str, str]
    roles: DjangoDocutilsLibRSTRolesSettings


class DjangoDocutilsLibTextSettings(TypedDict):
    """Core settings object for ``DJANGO_DOCUTILS_TEXT_RST``."""

    uncapitalized_word_filters: list[str]
