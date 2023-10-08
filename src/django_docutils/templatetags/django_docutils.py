"""Django template tag and filter for docutils (rendering reStructuredText as HTML)."""
import typing as t

from django import template
from django.template.base import FilterExpression, Node, Parser, Token, kwarg_re
from django.template.context import Context
from django.template.exceptions import TemplateSyntaxError
from django.utils.encoding import force_str
from django.utils.safestring import SafeString, mark_safe

from ..lib.publisher import publish_html_from_source

register = template.Library()


class ReStructuredTextNode(Node):
    """Implement the actions of the rst tag."""

    def __init__(
        self,
        content: t.Union[FilterExpression, str],
        args: t.Optional[list[FilterExpression]] = None,
        kwargs: t.Optional[dict[str, FilterExpression]] = None,
        asvar: str | None = None,
    ) -> None:
        self.content = content
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.asvar = asvar

    def render(self, context: t.Optional[Context] = None) -> str:
        """Render Node as string."""
        if context is None:
            context = Context()

        args = [arg.resolve(context) for arg in self.args]
        kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}

        if isinstance(self.content, FilterExpression):
            content = self.content.resolve(context)
        else:
            content = self.content

        html = publish_html_from_source(content, *args, **kwargs)
        if html is None:
            return ""
        return html


class MalformedArgumentsToRSTTag(TemplateSyntaxError):
    """Invalid arguments to rst django template tag."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        return super().__init__("Malformed arguments to url tag", *args, **kwargs)


@register.tag
def rst(parser: Parser, token: Token) -> ReStructuredTextNode:
    """Django template tag to render reStructuredText as HTML.

    Supports arguments, see below.

    Examples
    --------
    .. code-block:: django

        {% rst content %}

    .. code-block:: django

        {% rst content toc_only=True %}

    .. code-block:: django

        {% rst content show_title=False %}

    .. code-block:: django

        {% rst %}
        **Hello world**
        {% endrst %}

    Render table of contents:

    .. code-block:: django

        {% rst toc_only=True %}
        Welcome to my site!
        ===================

        My header
        ---------

        Some text

        Additional information
        ----------------------

        Thank you
        {% endrst %}
    """
    bits = token.split_contents()
    args = []
    kwargs = {}
    asvar = None

    content: t.Optional[t.Union[FilterExpression, SafeString]] = None

    if len(bits) >= 2 and bits[1] == "content":
        content = parser.compile_filter(bits[1])
        bits = bits[2:]  # Chop off "rst content"
    else:
        nodelist = parser.parse(("endrst",))
        parser.delete_first_token()
        content = nodelist.render(Context())
        bits = bits[1:]  # Chop off "rst"
    if len(bits) >= 2 and bits[-2] == "as":
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise MalformedArgumentsToRSTTag()

            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    # TODO: Raise if no end tag found
    # if len(bits) < 2:
    #     raise TemplateSyntaxError(
    #         "'%s' takes at least one argument, a content param." % bits[0]
    #     )

    return ReStructuredTextNode(content, args, kwargs, asvar)


@register.filter(name="rst", is_safe=True)
def rst_filter(value: str) -> str:
    """Django template filter to render reStructuredText (rst) as HTML."""
    import warnings

    warnings.warn(
        "The rst filter has been deprecated",
        category=DeprecationWarning,
        stacklevel=3,
    )

    return mark_safe(force_str(ReStructuredTextNode(value).render()))
