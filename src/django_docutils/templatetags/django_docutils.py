import typing as t

from django import template
from django.template.base import FilterExpression, Node, Parser, Token, kwarg_re
from django.template.context import Context
from django.template.exceptions import TemplateSyntaxError
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe

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


class MalformedArgumentsToUrlTag(TemplateSyntaxError):
    def __init__(self, *args: object, **kwargs: object) -> None:
        return super().__init__("Malformed arguments to url tag", *args, **kwargs)


@register.tag
def rst(parser: Parser, token: Token) -> ReStructuredTextNode:
    """Parse raw reStructuredText into HTML. Supports keyword arguments!

    Usage::

        {% rst content %}

        {% rst content toc_only=True %}

        {% rst content show_title=False %}

    Why does toc_only=true needed (why do you need to call twice just to get
    a ToC)? Because of how docutils parses.

    Passing content/params right into publish_html_from_source.
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(
            "'%s' takes at least one argument, a content param." % bits[0]
        )
    content = parser.compile_filter(bits[1])
    args = []
    kwargs = {}
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == "as":
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise MalformedArgumentsToUrlTag()

            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))
    return ReStructuredTextNode(content, args, kwargs, asvar)


@register.filter(name="rst", is_safe=True)
def rst_filter(value: str) -> str:
    import warnings

    warnings.warn(
        "The rst filter has been deprecated",
        category=DeprecationWarning,
        stacklevel=3,
    )

    return mark_safe(force_str(ReStructuredTextNode(value).render()))
