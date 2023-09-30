import typing as t

from _typeshed import Incomplete
from pygments.token import Other

if t.TYPE_CHECKING:
    from pygments.token import _TokenType

class _PseudoMatch:
    def __init__(self, start: str, text: str) -> None: ...
    def start(self, arg: Incomplete | None = None) -> int: ...
    def end(self, arg: Incomplete | None = None) -> int: ...
    def group(self, arg: Incomplete | None = None) -> t.AnyStr: ...
    def groups(self) -> tuple[t.AnyStr, ...]: ...
    def groupdict(self) -> dict[str, t.AnyStr]: ...

class Lexer:
    name: str | None = None
    aliases: list[str]
    filenames: list[str]
    alias_filenames: list[str]
    mime_types: list[str]
    priority: int
    ulr: str

    def __init__(
        self,
        options: dict[str, object] | None = {},  # noqa: B006
    ) -> None: ...

class RegexLexer(Lexer): ...
class ExtendedRegexLexer(RegexLexer): ...

class DelegatingLexer(Lexer):
    def __init__(
        self,
        _root_lexer: t.Any,
        _language_lexer: t.Any,
        _needle: t.Any = Other,
        **options: t.Any,
    ): ...

def bygroups(
    *args: Lexer | _TokenType,
) -> t.Generator[None, Lexer | _TokenType, None]: ...
def include(str: str) -> t.Any: ...
