"""Code related formatter and transformers."""
import re
import typing as t

from docutils import nodes
from docutils.transforms import Transform
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.token import Token

if t.TYPE_CHECKING:
    from collections.abc import Iterator

    from pygments.token import _TokenType

    TokenStream = Iterator[tuple[_TokenType, str]]
    TokenGenerator = Iterator[tuple[t.Union[str, int], str]]


class InlineHtmlFormatter(HtmlFormatter):  # type:ignore
    """HTMLFormatter for inline codeblocks."""

    def format_unencoded(self, tokensource: "TokenStream", outfile: t.Any) -> None:
        r"""Trim inline element of space and newlines.

        1. Trailing newline: Final token generated returns ``(Token.Other, '\n')``
           results in a blank space ``<span class="x"></span>``.

           This would be unnoticeable for a code block, but as this is inline, it looks
           strange. Let's filter out any trailing newlines from token source, then
           fallback to the normal process by passing it back into parent class method.
        2. Trailing space:

           *After* this method ``_format_lines`` still adds a ``\n`` (which renders as a
           space again in the browser). To suppress that pass ``lineseparator=''`` to
           the ``InlineHtmlFormatter`` class.
        """

        def filter_trailing_newline(source: "TokenStream") -> "TokenStream":
            tokens = list(source)

            # filter out the trailing newline token
            if tokens[-1] == (Token.Text, "\n"):
                del tokens[-1]

            return ((t, v) for t, v in tokens)

        source = filter_trailing_newline(tokensource)

        return super().format_unencoded(source, outfile)

    def _wrap_div(
        self,
        inner: "TokenStream",
    ) -> t.Union["TokenGenerator", "TokenStream"]:
        styles = []
        if (
            self.noclasses
            and not self.nobackground
            and self.style.background_color is not None
        ):
            styles.append(f"background: {self.style.background_color}")
        if self.cssstyles:
            styles.append(self.cssstyles)
        style = "; ".join(styles)

        yield (
            0,
            (
                "<span"
                + (self.cssclass and ' class="%s"' % self.cssclass)
                + (style and (' style="%s"' % style))
                + ">"
            ),
        )
        yield from inner
        yield 0, "</span>\n"

    def _wrap_pre(self, inner: "TokenStream") -> "TokenStream":
        yield from inner


formatter = InlineHtmlFormatter(
    cssclass="highlight docutils literal inline-code",
    noclasses=False,
    lineseparator="",  # removes \n from end of inline snippet
)


class CodeTransform(Transform):
    """Run over unparsed literals and try to guess language + highlight."""

    default_priority = 120

    def apply(self, **kwargs: t.Any) -> None:
        """Apply CodeTransform."""
        paragraph_nodes = self.document.traverse(nodes.literal)

        for node in paragraph_nodes:
            text = node.astext()

            newnode = None
            newtext = None
            newlexer: t.Any = None

            if text.startswith("$ "):
                from pygments.lexers.shell import BashSessionLexer

                from django_docutils.lib.directives.code import patch_bash_session_lexer

                patch_bash_session_lexer()

                newlexer = BashSessionLexer()
            elif text.startswith("{%") or text.startswith("{{"):
                from pygments.lexers.templates import DjangoLexer

                newlexer = DjangoLexer()
            elif re.match(r"^:\w+:", text):  # match :rolename: beginning
                from pygments.lexers.markup import RstLexer

                newlexer = RstLexer()  # type:ignore
            else:
                from pygments.lexers import guess_lexer
                from pygments.lexers.mime import MIMELexer
                from pygments.lexers.special import TextLexer

                guess = guess_lexer(text)
                if not any(guess.__class__ != lex for lex in [MIMELexer, TextLexer]):
                    newlexer = guess

            if newlexer:
                """Inline code can't have newlines, but we still get them:

                Take this reStructuredText code:

                .. code-block:: reStructuredText

                    You can set options with ``$ tmux set-option`` and ``$ tmux
                    set-window-option``.

                Docutils detects the separation between "tmux" and
                "set-window-option" in ``$ tmux set-window-options``, now as a
                 space, but a *new line*.

                Let's replace the newline escape (``\n``) with a space.
                """
                text = text.strip()  # trim any whitespace around text
                text = text.replace("\n", " ")  # switch out newlines w/ space

                newtext = highlight(text, newlexer, formatter)

            if newtext:
                newnode = nodes.raw("", newtext, format="html")

            if newnode and node.parent:
                node.replace_self(newnode)
