"""Typings for Django Docutils settings for django."""

from __future__ import annotations

import typing as t


class DjangoDocutilsLibRSTRolesSettings(t.TypedDict, total=False):
    """Docutils role mappings.

    Attributes
    ----------
    local : dict[str, str]
        Role name to import string of the callable implementing it, registered
        with docutils at startup and again whenever settings change.
    """

    local: dict[str, str]


class DjangoDocutilsLibRSTDocutilsSettings(t.TypedDict, total=False):
    """Docutils document settings.

    Attributes
    ----------
    file_insertion_enabled : bool
        Allow directives that read from the filesystem, such as ``include``.
        Held at ``False`` unless the project sets
        ``allow_unsafe_docutils_settings``.
    raw_enabled : bool
        Allow the ``raw`` directive and role to emit unescaped markup. Held at
        ``False`` unless the project sets ``allow_unsafe_docutils_settings``.
    _disable_config : bool
        Ignore ``docutils.conf`` files found on disk. Held at ``True`` unless
        the project sets ``allow_unsafe_docutils_settings``.
    line_length_limit : int
        Longest input line docutils will parse. Clamped back down to the
        django-docutils default unless the project sets
        ``allow_unsafe_docutils_settings``.
    strip_comments : bool
        Drop RST comments from the doctree instead of carrying them through to
        the output.
    initial_header_level : int
        HTML heading level a top-level section title renders as, so nested
        sections count up from there.
    """

    file_insertion_enabled: bool
    raw_enabled: bool
    _disable_config: bool
    line_length_limit: int
    strip_comments: bool
    initial_header_level: int


class DjangoDocutilsLibRSTSettings(t.TypedDict, total=False):
    """Core settings object for ``DJANGO_DOCUTILS_LIB_RST``.

    Attributes
    ----------
    allow_unsafe_docutils_settings : bool
        Opt in to overriding the protected docutils defaults and to keeping
        unsafe URI schemes in rendered output.
    allowed_uri_schemes : t.Sequence[str]
        URI schemes kept in rendered links and images. Unset means http,
        https, and mailto; unsafe schemes are stripped unless
        ``allow_unsafe_docutils_settings`` is set.
    metadata_processors : list[str]
        Import strings of callables applied in order to a document's extracted
        metadata, each taking and returning the metadata mapping.
    transforms : list[str]
        Import strings of :class:`docutils.transforms.Transform` subclasses
        appended to the writer's transforms.
    docutils : DjangoDocutilsLibRSTDocutilsSettings
        Docutils publisher settings layered over the django-docutils defaults.
    directives : dict[str, str]
        Directive name to import string of the
        :class:`docutils.parsers.rst.Directive` subclass registered for it.
    roles : DjangoDocutilsLibRSTRolesSettings
        Role registrations, grouped by the scope they are registered in.
    """

    allow_unsafe_docutils_settings: bool
    allowed_uri_schemes: t.Sequence[str]
    metadata_processors: list[str]
    transforms: list[str]
    docutils: DjangoDocutilsLibRSTDocutilsSettings
    directives: dict[str, str]
    roles: DjangoDocutilsLibRSTRolesSettings


class DjangoDocutilsLibTextSettings(t.TypedDict):
    """Core settings object for ``DJANGO_DOCUTILS_LIB_TEXT``.

    Attributes
    ----------
    uncapitalized_word_filters : list[str]
        Import strings of predicates taking a single word. A filter returning
        ``True`` keeps that word as-authored during title casing; an empty list
        capitalizes every word.
    """

    uncapitalized_word_filters: list[str]
