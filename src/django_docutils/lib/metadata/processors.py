import datetime

import pytz
from django.conf import settings


def process_datetime(metadata):
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
            metadata[time_key] = pytz.timezone(settings.TIME_ZONE).localize(
                metadata[time_key], is_dst=None
            )
    return metadata


def process_anonymous_user(metadata):
    """Corrects name of author "anonymous" to django's anonymous username"""

    if metadata.get("author", None) == "anonymous":
        metadata["author"] = settings.ANONYMOUS_USER_NAME

    return metadata
