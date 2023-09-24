from django import template
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe

from django_docutils.exc import DocutilsNotInstalled

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
