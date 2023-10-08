"""Metadata processing for Django Docutils."""
import datetime
import typing as t

from django.conf import settings

HAS_PYTZ = False
try:
    import pytz

    HAS_PYTZ = True
except ImportError:
    pass


def process_datetime(metadata: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
    """Optionally supports localizing times via pytz."""
    timezone_formats = [  # timezone formats to try, most detailed to least
        "%Y-%m-%d %I:%M%p",
        "%Y-%m-%d",
    ]

    for time_key in ["created", "modified"]:
        if time_key in metadata:
            for _format in timezone_formats:
                try:
                    metadata[time_key] = datetime.datetime.strptime(
                        metadata[time_key], _format
                    )
                    break
                except ValueError:
                    continue

            if HAS_PYTZ:
                metadata[time_key] = pytz.timezone(settings.TIME_ZONE).localize(
                    metadata[time_key], is_dst=None
                )
    return metadata


def process_anonymous_user(metadata: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
    """Corrects name of author "anonymous" to django's anonymous username."""
    if metadata.get("author", None) == "anonymous" and hasattr(
        settings, "DJANGO_DOCUTIL_ANONYMOUS_USER_NAME"
    ):
        metadata["author"] = settings.DJANGO_DOCUTILS_ANONYMOUS_USER_NAME

    return metadata
