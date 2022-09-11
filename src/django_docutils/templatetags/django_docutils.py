from django import template
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def restructuredtext(value):
    import warnings

    warnings.warn(
        "The restructuredtext filter has been deprecated", category=DeprecationWarning
    )
    try:
        from docutils.core import publish_parts
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError(
                "Error in 'restructuredtext' filter: The Python docutils "
                "library isn't installed."
            )
        return force_str(value)
    else:
        docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
        parts = publish_parts(
            source=force_bytes(value),
            writer_name="html5_polyglot",
            settings_overrides=docutils_settings,
        )
        return mark_safe(force_str(parts["fragment"]))
