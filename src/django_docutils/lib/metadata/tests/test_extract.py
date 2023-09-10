from django.utils.encoding import force_bytes
from docutils.core import publish_doctree

from django_docutils.lib.metadata.extract import (
    extract_metadata,
    extract_subtitle,
    extract_title,
)
from django_docutils.lib.settings import DJANGO_DOCUTILS_LIB_RST


def test_extract_title():
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


def test_extract_subtitle():
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


def test_extract_metadata(tmp_path):
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
        source=force_bytes(content), settings_overrides=docutils_settings
    )

    assert extract_metadata(doctree) == {
        "programming_languages": "javascript",
        "topics": "webpack",
        "created": "2017-07-30",
        "author": "tony",
    }
