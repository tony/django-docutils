from django import template
from django.template.base import kwarg_re
from django.template.defaulttags import Node
from django.template.exceptions import TemplateSyntaxError

from ..publisher import publish_html_from_source

register = template.Library()


class ReStructuredTextNode(Node):

    """Implement the actions of the rst tag."""

    def __init__(self, content, args, kwargs, asvar):
        self.content = content
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}

        content = self.content.resolve(context)

        return publish_html_from_source(content, *args, **kwargs)


@register.tag
def restructuredtext(parser, token):
    """Parse raw reStructuredText into HTML. Supports keyword arguments!

    Usage::

        {% restructuredtext content %}

        {% restructuredtext content inject_ads=False %}

        {% restructuredtext content toc_only=True %}

        {% restructuredtext content show_title=False %}

        {% restructuredtext content inject_ads=True ad_keywords=ad_keywords %}

    Why does toc_only=true needed (why do you need to call twice just to get
    a ToC)? Because of how docutils parses.

    Passing content/params right into publish_html_from_source.
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(
            "'%s' takes at least one argument, a URL pattern name." % bits[0]
        )
    content = parser.compile_filter(bits[1])
    args = []
    kwargs = {}
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError('Malformed arguments to url tag')
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))
    return ReStructuredTextNode(content, args, kwargs, asvar)
