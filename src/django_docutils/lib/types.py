import typing as t

from typing_extensions import NotRequired, TypedDict


class DjangoDocutilsLibRSTRolesSettings(TypedDict):
    local: NotRequired[t.Dict[str, str]]


class DjangoDocutilsLibRSTDocutilsSettings(TypedDict):
    raw_enabled: NotRequired[bool]
    strip_comments: NotRequired[bool]
    initial_header_level: NotRequired[int]


class DjangoDocutilsLibRSTFontAwesomeSettings(TypedDict):
    url_patterns: NotRequired[t.Dict[str, str]]


class DjangoDocutilsLibRSTSettings(TypedDict):
    metadata_processors: NotRequired[list[str]]
    transforms: NotRequired[list[str]]
    docutils: NotRequired[DjangoDocutilsLibRSTDocutilsSettings]
    directives: NotRequired[t.Dict[str, str]]
    roles: NotRequired[DjangoDocutilsLibRSTRolesSettings]
    font_awesome: NotRequired[DjangoDocutilsLibRSTFontAwesomeSettings]


class DjangoDocutilsLibTextSettings(TypedDict):
    uncapitalized_word_filters: list[str]
