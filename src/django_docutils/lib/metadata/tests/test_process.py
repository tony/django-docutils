import datetime

from django.utils.encoding import force_bytes
from docutils.core import publish_doctree

from django_docutils.lib.metadata.extract import extract_metadata
from django_docutils.lib.metadata.process import process_metadata


def test_process_metadata_file():
    source = """
===========
Content ok!
===========

:programming_language: javascript
:topic: webpack
:Created: 2017-07-30
:Author: tony

more text

first section
-------------

some content
""".strip()

    doctree = publish_doctree(source=force_bytes(source))

    raw_metadata = extract_metadata(doctree)

    analyzed_metadata = process_metadata(raw_metadata.copy())
    assert set(raw_metadata.keys()) == set(analyzed_metadata.keys())

    assert isinstance(analyzed_metadata["created"], datetime.date)

    assert process_metadata(raw_metadata) != {
        "programming_languages": "javascript",
        "topics": "webpack",
        "created": "2017-07-30",
        "author": "tony",
    }


def test_process_metadata_daytime_timezone():
    """Verify time of day and timezone (optional) work with dates."""

    source = """
===========
Content ok!
===========

:programming_language: javascript
:topic: webpack
:Created: 2017-07-30 2:30PM
:Author: tony

more text

first section
-------------

some content
""".strip()

    doctree = publish_doctree(source=force_bytes(source))

    raw_metadata = extract_metadata(doctree)

    analyzed_metadata = process_metadata(raw_metadata.copy())
    assert set(raw_metadata.keys()) == set(analyzed_metadata.keys())

    created = analyzed_metadata["created"]

    assert isinstance(created, datetime.date)
    assert created.year == 2017
    assert created.month == 7
    assert created.day == 30
    assert created.strftime("%I") == "02"
    assert created.strftime("%p") == "PM"
    assert created.minute == 30
