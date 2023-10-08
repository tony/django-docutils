"""Tests for Django Docutils Writers."""
from django.utils.encoding import force_bytes
from docutils.core import publish_doctree
from docutils.writers.html5_polyglot import Writer

from ..publisher import publish_parts_from_doctree
from ..settings import DJANGO_DOCUTILS_LIB_RST
from ..writers import DjangoDocutilsWriter


def test_HTMLWriter_hides_docinfo() -> None:
    """Assert HTMLWriter hides docinfo."""
    docutils_settings = DJANGO_DOCUTILS_LIB_RST.get("docutils", {})

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

    doctree = publish_doctree(
        source=force_bytes(content), settings_overrides=docutils_settings
    )

    # Test that normal writer will show docinfo in HTML
    parts = publish_parts_from_doctree(
        doctree, writer=Writer(), settings_overrides=docutils_settings
    )
    assert "key1" in parts["html_body"]

    # Our writer should *not* output docinto
    parts = publish_parts_from_doctree(
        doctree, writer=DjangoDocutilsWriter(), settings_overrides=docutils_settings
    )

    assert "key1" not in parts["html_body"]
    assert "first section" in parts["html_body"]
