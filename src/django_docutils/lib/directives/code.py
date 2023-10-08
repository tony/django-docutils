"""Pygments docutils directive.

The Pygments reStructuredText directive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

This fragment is a `Docutils <https://docutils.sourceforge.io/>`_ 0.5 directive that 
renders source code (to HTML only, currently) via Pygments.

To use it, adjust the options below and copy the code into a module
that you import on initialization.  The code then automatically
registers a ``sourcecode`` directive that you can use instead of
normal code blocks like this:

.. code-block:: rst

    .. sourcecode:: python

       My code goes here.

If you want to have different code styles, e.g. one with line numbers
and one without, add formatters with their names in the ``VARIANTS`` dict
below.  You can invoke them instead of the ``DEFAULT`` one by using a
directive option:

.. code-block:: rst

   .. sourcecode:: python
      :linenos:

      My code goes here.

Look at the `directive documentation <https://docutils.sourceforge.io/docs/ref/rst/directives.html>`_
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
from pygments.lexers.special import TextLexer

if t.TYPE_CHECKING:
    from pygments.formatter import Formatter


def patch_bash_session_lexer() -> None:
    """Monkey patch Bash Session lexer to gobble up initial space after prompt."""
    from pygments.lexers.shell import BashSessionLexer

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
VARIANTS: t.Dict[str, "Formatter[str]"] = {
    # 'linenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=True),
}

DEFAULT_OPTION_SPEC: t.Dict[str, t.Callable[[str], t.Any]] = {
    key: directives.flag for key in VARIANTS
}


class CodeBlock(Directive):
    """Source code syntax highlighting."""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = DEFAULT_OPTION_SPEC
    has_content = True

    def run(self) -> list[nodes.Node]:
        """Directive run method for CodeBlock."""
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


def register_pygments_directive(directive: str = "code-block") -> None:
    """Register pygments directive.

    Parameters
    ----------
    directive : str
        directive name to register pygments to.

    Examples
    --------
    If you wish to use (override) code-block (default), that means:

    .. code-block:: rst

        .. code-block::

            // will be highlighted by pygments
    """
    directives.register_directive(directive, CodeBlock)
