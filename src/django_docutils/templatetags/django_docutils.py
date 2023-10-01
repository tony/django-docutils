from django import template
from django.template.context import Context
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe

from ..lib.templatetags.rst import ReStructuredTextNode

register = template.Library()


@register.filter(is_safe=True)
def rst(value: str) -> str:
    """RestructuredText Filter

    Credit
    ------
    Thank you readthedocs.org.

    Belated credit (2023-10-01), via GitHub Search, I see readthedocs.org, had this in
    `8609c16 <https://github.com/readthedocs/readthedocs.org/commit/8609c16db5c7d92cb5272addab1910a6eddbb2f1>`_,
    with an `MIT license <https://github.com/readthedocs/readthedocs.org/blob/8609c16db5c7d92cb5272addab1910a6eddbb2f1/LICENSE.mit>`_.
    """
    import warnings

    warnings.warn(
        "The rst filter has been deprecated",
        category=DeprecationWarning,
        stacklevel=3,
    )

    return mark_safe(
        force_str(ReStructuredTextNode(value, [], {}, None).render(Context({})))
    )
