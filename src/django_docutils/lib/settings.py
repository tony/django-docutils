from django.conf import settings

DJANGO_DOCUTILS_LIB_RST = getattr(settings, "DJANGO_DOCUTILS_LIB_RST", {})

INJECT_FONT_AWESOME = (
    DJANGO_DOCUTILS_LIB_RST.get("font_awesome", {}).get("url_patterns") is not None
)
