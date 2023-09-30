import typing as t

if t.TYPE_CHECKING:
    from pygments.token import _TokenType

class Lexer:
    name: str | None = None
    aliases: list[str]
    filenames: list[str]
    alias_filenames: list[str]
    mime_types: list[str]
    priority: int
    ulr: str

    def __init__(self, options: dict[str, object] | None = {}) -> None: ...

class RegexLexer(Lexer): ...

def bygroups(
    *args: Lexer | _TokenType,
) -> t.Generator[None, Lexer | _TokenType, None]: ...
