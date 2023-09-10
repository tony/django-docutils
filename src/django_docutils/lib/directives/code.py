"""
The Pygments reStructuredText directive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This fragment is a `Docutils <ttps://docutils.sf.net/>`_ 0.5 directive
that renders source code (to HTML only, currently) via Pygments.

To use it, adjust the options below and copy the code into a module
that you import on initialization.  The code then automatically
registers a ``sourcecode`` directive that you can use instead of
normal code blocks like this::

    .. sourcecode:: python

       My code goes here.

If you want to have different code styles, e.g. one with line numbers
and one without, add formatters with their names in the VARIANTS dict
below.  You can invoke them instead of the DEFAULT one by using a
directive option::

    .. sourcecode:: python

       :linenos:

       My code goes here.

Look at the `directive documentation
<http://docutils.sourceforge.net/docs/howto/rst-directives.html>`_
to get all the gory details.

:copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""
import re
import typing as t

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.shell import BashSessionLexer
from pygments.lexers.special import TextLexer

if t.TYPE_CHECKING:
    from pygments.formatter import Formatter


#: Monkey patch Bash Session lexer to gobble up initial space after prompt
BashSessionLexer._ps1rgx = re.compile(
    r"^((?:(?:\[.*?\])|(?:\(\S+\))?(?:| |sh\S*?|\w+\S+[@:]\S+(?:\s+\S+)"
    r"?|\[\S+[@:][^\n]+\].+))\s*[$#%] )(.*\n?)"
)

# Options
# ~~~~~~~

#: Set to True if you want inline CSS styles instead of classes
INLINESTYLES = False

#: The default formatter
DEFAULT = HtmlFormatter(cssclass="highlight code-block", noclasses=INLINESTYLES)

#: Add name -> formatter pairs for every variant you want to use
VARIANTS: t.Dict[str, t.Type["Formatter"]] = {
    # 'linenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=True),
}


class CodeBlock(Directive):

    """Source code syntax highlighting."""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: t.ClassVar = {key: directives.flag for key in VARIANTS}
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer_name = self.arguments[0]

            lexer = get_lexer_by_name(lexer_name)
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()
        # take an arbitrary option if more than one is given
        formatter = self.options and VARIANTS[next(iter(self.options))] or DEFAULT
        parsed = highlight("\n".join(self.content), lexer, formatter)
        return [nodes.raw("", parsed, format="html")]
