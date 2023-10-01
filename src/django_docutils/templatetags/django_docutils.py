from django import template
from django.template.context import Context
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe

from ..lib.templatetags.rst import ReStructuredTextNode

register = template.Library()


@register.filter(is_safe=True)
def restructuredtext(value: str) -> str:
    import warnings

    warnings.warn(
        "The restructuredtext filter has been deprecated",
        category=DeprecationWarning,
        stacklevel=3,
    )

    return mark_safe(
        force_str(ReStructuredTextNode(value, [], {}, None).render(Context({})))
    )
