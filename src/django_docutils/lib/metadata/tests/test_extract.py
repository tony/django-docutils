"""Test metadata and title extraction from reStructuredText."""
import pathlib

from django.utils.encoding import force_bytes
from docutils.core import publish_doctree

from ...settings import DJANGO_DOCUTILS_LIB_RST
from ..extract import (
    extract_metadata,
    extract_subtitle,
    extract_title,
)


def test_extract_title() -> None:
    """Assert title extraction from reStructuredText."""
    content = """
===========
Hello world
===========

:key1: value
:key2: value

more text

first section
-------------

some content
""".strip()

    doctree = publish_doctree(source=force_bytes(content))

    assert extract_title(doctree) == "Hello world"


def test_extract_subtitle() -> None:
    """Assert subtitle extraction from reStructuredText."""
    content = """
===========
Hello world
===========
moo
===

:key1: value
:key2: value

more text

first section
-------------

some content
""".strip()

    doctree = publish_doctree(source=force_bytes(content))

    assert extract_subtitle(doctree) == "moo"


def test_extract_metadata(tmp_path: pathlib.Path) -> None:
    """Assert metadata extraction from reStructuredText."""
    docutils_settings = DJANGO_DOCUTILS_LIB_RST.get("docutils", {})
    content = """
===========
Content ok!
===========

:programming_languages: javascript
:topics: webpack
:Created: 2017-07-30
:Author: tony

more text

first section
-------------

some content
""".strip()

    doctree = publish_doctree(
        source=force_bytes(content),
        settings_overrides=docutils_settings,
    )

    assert extract_metadata(doctree) == {
        "programming_languages": "javascript",
        "topics": "webpack",
        "created": "2017-07-30",
        "author": "tony",
    }
