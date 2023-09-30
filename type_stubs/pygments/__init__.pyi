import typing as t

from _typeshed import SupportsWrite
from pygments.formatter import Formatter
from pygments.lexer import Lexer

_T = t.TypeVar("_T", str, bytes)

@t.overload
def highlight(
    code: t.Any,
    lexer: Lexer,
    formatter: Formatter[_T],
) -> str: ...
@t.overload
def highlight(
    code: t.Any,
    lexer: Lexer,
    formatter: Formatter[_T],
    outfile: SupportsWrite[_T],
) -> str: ...
@t.overload
def highlight(
    code: t.Any,
    lexer: Lexer,
    formatter: Formatter[_T],
    outfile: None,
) -> str: ...
