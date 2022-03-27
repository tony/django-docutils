import re

from docutils import nodes
from docutils.transforms import Transform
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.token import Token


class InlineHtmlFormatter(HtmlFormatter):
    def format_unencoded(self, tokensource, outfile):
        """

        First problem (filter trailing newline):

        There is an issue where the final token generated returns a
        (Token.Other, '\n') which results in a blank space
        <span class="x"></span>

        This would otherwise be unnoticeable if it was a code block,
        but since we're inline, it looks strange. Let's filter out
        any trailing newlines from token source, then fallback to
        the normal process by passing it back into parent class method.

        Now, AFTER this method, you're not out of the woods yet:
        _format_lines will still add a \n (which renders as a space again
        in the browser). For that, pass lineseparator='' into the
        InlineHtmlFormatter class to supress that.

        """

        def filter_trailing_newline(source):
            tokens = list(source)

            # filter out the trailing newline token
            if tokens[-1] == (Token.Text, "\n"):
                del tokens[-1]

            return ((t, v) for t, v in tokens)

        source = filter_trailing_newline(tokensource)

        return super().format_unencoded(source, outfile)

    def _wrap_div(self, inner):
        style = []
        if (
            self.noclasses
            and not self.nobackground
            and self.style.background_color is not None
        ):
            style.append(f"background: {self.style.background_color}")
        if self.cssstyles:
            style.append(self.cssstyles)
        style = "; ".join(style)

        yield 0, (
            "<span"
            + (self.cssclass and ' class="%s"' % self.cssclass)
            + (style and (' style="%s"' % style))
            + ">"
        )
        yield from inner
        yield 0, "</span>\n"

    def _wrap_pre(self, inner):
        yield from inner


formatter = InlineHtmlFormatter(
    cssclass="highlight docutils literal inline-code",
    noclasses=False,
    lineseparator="",  # removes \n from end of inline snippet
)


class CodeTransform(Transform):

    """Run over unparsed literals and try to guess language + highlight."""

    default_priority = 120

    def apply(self):
        paragraph_nodes = self.document.traverse(nodes.literal)

        for node in paragraph_nodes:
            text = node.astext()

            newnode = None
            newtext = None
            newlexer = None

            if text.startswith("$ "):
                from django_docutils.lib.directives.code import BashSessionLexer

                newlexer = BashSessionLexer()
            elif text.startswith("{%") or text.startswith("{{"):
                from pygments.lexers.templates import DjangoLexer

                newlexer = DjangoLexer()
            elif re.match(r"^:\w+:", text):  # match :rolename: beginning
                from pygments.lexers.markup import RstLexer

                newlexer = RstLexer()
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
