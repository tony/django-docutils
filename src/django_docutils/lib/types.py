"""Typings for Django Docutils settings for django."""
import typing as t

from typing_extensions import NotRequired, TypedDict


class DjangoDocutilsLibRSTRolesSettings(TypedDict):
    """Docutils role mappings."""

    local: NotRequired[t.Dict[str, str]]


class DjangoDocutilsLibRSTDocutilsSettings(TypedDict):
    """Docutils document settings."""

    raw_enabled: NotRequired[bool]
    strip_comments: NotRequired[bool]
    initial_header_level: NotRequired[int]


class DjangoDocutilsLibRSTSettings(TypedDict):
    """Core settings object for ``DJANGO_DOCUTILS_LIB_RST``."""

    metadata_processors: NotRequired[list[str]]
    transforms: NotRequired[list[str]]
    docutils: NotRequired[DjangoDocutilsLibRSTDocutilsSettings]
    directives: NotRequired[t.Dict[str, str]]
    roles: NotRequired[DjangoDocutilsLibRSTRolesSettings]


class DjangoDocutilsLibTextSettings(TypedDict):
    """Core settings object for ``DJANGO_DOCUTILS_TEXT_RST``."""

    uncapitalized_word_filters: list[str]
