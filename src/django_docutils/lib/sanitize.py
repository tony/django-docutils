"""Doctree sanitization for Django Docutils web-facing rendering.

These helpers strip HTML-unsafe nodes and attributes from a docutils
document before it is written to HTML. :class:`SanitizeTransform` exposes the
same pass as a docutils transform so it can run inside a custom writer
pipeline; :func:`sanitize_doctree` is the reusable entry point.
"""

from __future__ import annotations

import typing as t
import urllib.parse

from docutils import nodes
from docutils.transforms import Transform

from .settings import (
    get_allowed_uri_schemes,
    get_docutils_settings,
    unsafe_docutils_settings_allowed,
)

_C0_CONTROL_CHARS: t.Final[frozenset[str]] = frozenset(
    chr(code_point) for code_point in range(0x20)
) | {"\x7f"}
"""C0 / DEL control characters that disqualify a URI outright."""


def _uri_is_allowed(uri: str, allowed_uri_schemes: frozenset[str]) -> bool:
    r"""Return whether a URI can be emitted into HTML attributes.

    Control characters are rejected before parsing: scheme-invalid bytes
    such as a vertical tab make ``urlsplit`` report an empty scheme, which
    would otherwise pass as a relative link. URIs ``urlsplit`` refuses to
    parse (e.g. malformed IPv6 brackets) are treated as disallowed.

    Examples
    --------
    >>> _uri_is_allowed("https://example.com", frozenset({"https"}))
    True
    >>> _uri_is_allowed("#section", frozenset())
    True
    >>> _uri_is_allowed("javascript:alert(1)", frozenset({"https"}))
    False
    >>> _uri_is_allowed("java\x0bscript:alert(1)", frozenset({"https"}))
    False
    >>> _uri_is_allowed("http://[::1", frozenset({"http"}))
    False
    """
    if any(char in _C0_CONTROL_CHARS for char in uri):
        return False
    try:
        parts = urllib.parse.urlsplit(uri)
    except ValueError:
        return False
    if not parts.scheme:
        return True
    return parts.scheme.lower() in allowed_uri_schemes


def _replace_node_with_text(node: nodes.Element) -> None:
    """Replace a node with its rendered text content.

    Examples
    --------
    >>> paragraph = nodes.paragraph()
    >>> reference = nodes.reference("", "", nodes.Text("link"))
    >>> paragraph += reference
    >>> _replace_node_with_text(reference)
    >>> paragraph.astext()
    'link'
    """
    if node.parent is None:
        return
    node.parent.replace(node, nodes.Text(node.astext()))


def _remove_node(node: nodes.Element) -> None:
    """Remove a node from its parent if it is attached.

    Examples
    --------
    >>> paragraph = nodes.paragraph()
    >>> raw = nodes.raw("", "<script></script>", format="html")
    >>> paragraph += raw
    >>> _remove_node(raw)
    >>> len(paragraph.children)
    0
    """
    if node.parent is not None:
        node.parent.remove(node)


def sanitize_doctree(
    document: nodes.document,
    docutils_settings: t.Mapping[str, object] | None = None,
) -> None:
    """Remove unsafe HTML-producing nodes and attributes from a doctree.

    Parameters
    ----------
    document : docutils.nodes.document
        Doctree to sanitize in place.
    docutils_settings : mapping, optional
        Already-resolved Docutils settings, consumed as-is. ``None``
        resolves project defaults via :func:`get_docutils_settings`.
        ``raw_enabled`` only skips raw-node removal when the project also
        sets ``allow_unsafe_docutils_settings``. URI scheme policy is
        project-level via :func:`get_allowed_uri_schemes`, not per-call.

    Examples
    --------
    >>> document = nodes.document("", "")
    >>> document += nodes.raw("", "<script></script>", format="html")
    >>> sanitize_doctree(document)
    >>> len(document.children)
    0
    """
    settings = (
        dict(docutils_settings)
        if docutils_settings is not None
        else get_docutils_settings()
    )
    allowed_uri_schemes = get_allowed_uri_schemes()

    raw_skip_allowed = (
        settings.get("raw_enabled") is True and unsafe_docutils_settings_allowed()
    )
    if not raw_skip_allowed:
        for raw_node in list(document.findall(nodes.raw)):
            if raw_node.get("django_docutils_trusted_raw") is not True:
                _remove_node(raw_node)

    for reference in list(document.findall(nodes.reference)):
        refuri = reference.get("refuri")
        if isinstance(refuri, str) and not _uri_is_allowed(
            refuri,
            allowed_uri_schemes,
        ):
            _replace_node_with_text(reference)

    for target in list(document.findall(nodes.target)):
        refuri = target.get("refuri")
        if isinstance(refuri, str) and not _uri_is_allowed(refuri, allowed_uri_schemes):
            del target["refuri"]

    for image in list(document.findall(nodes.image)):
        uri = image.get("uri")
        if isinstance(uri, str) and not _uri_is_allowed(uri, allowed_uri_schemes):
            _remove_node(image)


class SanitizeTransform(Transform):
    """Run :func:`sanitize_doctree` as a docutils transform.

    :class:`~django_docutils.lib.writers.DjangoDocutilsWriter` sanitizes in
    ``translate()`` so the pass always runs after every transform. This
    transform makes the same pass available to custom docutils pipelines that
    do not use that writer. ``default_priority`` is high so it runs late when
    added to a writer's transform list.

    Examples
    --------
    >>> from django_docutils.lib.publisher import publish_doctree
    >>> document = publish_doctree("Hello")
    >>> document += nodes.raw("", "<script></script>", format="html")
    >>> SanitizeTransform(document, document).apply()
    >>> list(document.findall(nodes.raw))
    []
    """

    default_priority = 990

    def apply(self, **kwargs: t.Any) -> None:
        """Sanitize the document tree in place."""
        sanitize_doctree(self.document)
