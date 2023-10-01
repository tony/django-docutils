from django import template
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe

from ..exc import DocutilsNotInstalled

register = template.Library()


class ReStructuredTextLibraryMissingForDjangoFilter(
    DocutilsNotInstalled, template.TemplateSyntaxError, ImportError
):
    def __init__(self, *args: object, **kwargs: object) -> None:
        return super().__init__(
            "Error in 'restructuredtext' filter: "
            "The Python docutils library isn't installed",
            *args,
            **kwargs
        )


@register.filter(is_safe=True)
def restructuredtext(value: str) -> str:
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
        "The restructuredtext filter has been deprecated",
        category=DeprecationWarning,
        stacklevel=2,
    )
    try:
        from docutils.core import publish_parts
    except ImportError as e:
        if settings.DEBUG:
            raise ReStructuredTextLibraryMissingForDjangoFilter() from e
        return force_str(value)
    else:
        docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
        parts = publish_parts(
            source=force_bytes(value),
            writer_name="html5_polyglot",
            settings_overrides=docutils_settings,
        )

        assert isinstance(parts["fragment"], str)

        return mark_safe(force_str(parts["fragment"]))
