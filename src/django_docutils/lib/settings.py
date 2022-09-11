from django.conf import settings

BASED_LIB_RST = getattr(settings, "BASED_LIB_RST", {})

INJECT_FONT_AWESOME = (
    BASED_LIB_RST.get("font_awesome", {}).get("url_patterns") is not None
)
