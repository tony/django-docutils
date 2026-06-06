"""Typings for Django Docutils settings for django."""

from __future__ import annotations

import typing as t

from typing_extensions import NotRequired, TypedDict


class DjangoDocutilsLibRSTRolesSettings(TypedDict, total=False):
    """Docutils role mappings."""

    local: dict[str, str]


class DjangoDocutilsLibRSTDocutilsSettings(TypedDict, total=False):
    """Docutils document settings."""

    file_insertion_enabled: bool
    raw_enabled: bool
    _disable_config: bool
    line_length_limit: int
    strip_comments: bool
    initial_header_level: int


class DjangoDocutilsLibRSTSettings(TypedDict, total=False):
    """Core settings object for ``DJANGO_DOCUTILS_LIB_RST``."""

    allow_unsafe_docutils_settings: bool
    allowed_uri_schemes: NotRequired[t.Sequence[str]]
    metadata_processors: list[str]
    transforms: list[str]
    docutils: DjangoDocutilsLibRSTDocutilsSettings
    directives: dict[str, str]
    roles: DjangoDocutilsLibRSTRolesSettings


class DjangoDocutilsLibTextSettings(TypedDict):
    """Core settings object for ``DJANGO_DOCUTILS_TEXT_RST``."""

    uncapitalized_word_filters: list[str]
