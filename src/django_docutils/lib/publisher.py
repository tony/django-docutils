"""Docutils Publisher fors for Django Docutils."""

from __future__ import annotations

import typing as t
import urllib.parse

from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe
from docutils import io, nodes, writers
from docutils.core import Publisher, publish_doctree as docutils_publish_doctree
from docutils.readers.doctree import Reader
from typing_extensions import NotRequired, TypedDict, Unpack

from .directives.registry import register_django_docutils_directives
from .roles.registry import register_django_docutils_roles
from .settings import get_allowed_uri_schemes, get_docutils_settings
from .transforms.toc import Contents
from .writers import DjangoDocutilsWriter

_C0_CONTROL_CHARS: t.Final[frozenset[str]] = frozenset(
    chr(code_point) for code_point in range(0x20)
) | {"\x7f"}
"""C0 / DEL control characters that disqualify a URI outright."""


def _uri_is_allowed(uri: str, allowed_uri_schemes: frozenset[str]) -> bool:
    r"""Return whether a URI can be emitted into HTML attributes.

    Control characters are rejected before parsing: scheme-invalid bytes
    such as a vertical tab make ``urlsplit`` report an empty scheme, which
    would otherwise pass as a relative link.

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
    """
    if any(char in _C0_CONTROL_CHARS for char in uri):
        return False
    parts = urllib.parse.urlsplit(uri)
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
        URI scheme policy is project-level via
        :func:`get_allowed_uri_schemes`, not per-call.

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

    if settings.get("raw_enabled") is not True:
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


def publish_parts_from_doctree(
    document: nodes.document,
    destination_path: str | None = None,
    writer: writers.Writer | None = None,
    writer_name: str = "pseudoxml",
    settings: t.Any | None = None,
    settings_spec: t.Any | None = None,
    settings_overrides: t.Mapping[str, object] | None = None,
    config_section: str | None = None,
    enable_exit_status: bool = False,
) -> dict[str, str]:
    """Render docutils doctree into docutils parts.

    Examples
    --------
    >>> doctree = publish_doctree("Hello **world**")
    >>> parts = publish_parts_from_doctree(doctree, writer=DjangoDocutilsWriter())
    >>> "world" in parts["html_body"]
    True
    """
    docutils_settings = get_docutils_settings(settings_overrides)
    sanitize_doctree(document, docutils_settings)
    if settings is not None:
        for setting, value in docutils_settings.items():
            setattr(settings, setting, value)

    reader = Reader(parser_name="null")  # type:ignore
    pub = Publisher(
        reader,
        None,
        writer,
        source=io.DocTreeInput(document),
        destination_class=io.StringOutput,
        settings=settings,
    )
    if not writer and writer_name:
        pub.set_writer(writer_name)
    pub.process_programmatic_settings(
        settings_spec,
        docutils_settings,
        config_section,
    )
    pub.set_destination(None, destination_path)
    pub.publish(enable_exit_status=enable_exit_status)
    return pub.writer.parts  # type:ignore


def publish_toc_from_doctree(
    doctree: nodes.document,
    writer: writers.Writer | None = None,
) -> str | None:
    """Publish table of contents from docutils doctree."""
    if not writer:
        writer = DjangoDocutilsWriter()
    # Create a new document tree with just the table of contents
    # ==========================================================

    # document tree template:
    toc_tree = nodes.document(
        "",  # type:ignore
        "",  # type:ignore
        source="toc-generator",
        classes=["fixed-toc-menu menu"],
    )
    toc_tree += nodes.paragraph("", "Contents", classes=["menu-label"])
    # Set up a Contents instance:
    # The Contents transform requires a "pending" startnode and
    # generation options startnode
    pending = nodes.pending(Contents, rawsource="")  # type:ignore

    contents_transform = Contents(doctree, pending)

    # this assures we get backlinks pointing to themselves
    # so users can copy anchor from headers
    contents_transform.backlinks = "entry"

    toc_contents = contents_transform.build_contents(doctree)

    if not toc_contents:  # ToC is empty
        return None

    # run the contents builder and append the result to the template:
    toc_topic = nodes.topic(classes=["contents", "toc"])

    toc_topic += toc_contents
    toc_tree += toc_topic
    toc = publish_parts_from_doctree(toc_tree, writer=writer)
    return mark_safe(force_str(toc["html_body"]))


def publish_doctree(
    source: str | bytes,
    settings_overrides: t.Mapping[str, object] | None = None,
) -> nodes.document:
    """Split off ability to get doctree (a.k.a. document).

    It's valuable to be able to run transforms to alter and most importantly,
    extract data like post abstracts.

    Parameters
    ----------
    source : str or bytes
        RST content
    settings_overrides : dict
        Settings overrides for docutils

    Returns
    -------
    docutils.nodes.document
        document/doctree for reStructuredText content

    Examples
    --------
    >>> doctree = publish_doctree("Hello **world**")
    >>> doctree.astext().startswith("Hello")
    True
    """
    register_django_docutils_directives()
    register_django_docutils_roles()
    docutils_settings = get_docutils_settings(settings_overrides)

    return docutils_publish_doctree(  # type:ignore
        source=force_bytes(source),
        settings_overrides=docutils_settings,
    )


class PublishHtmlDocTreeKwargs(TypedDict):
    """Keyword arguments accepted by publish_html_from_source."""

    show_title: NotRequired[bool]
    toc_only: NotRequired[bool]


def publish_html_from_source(
    source: str,
    **kwargs: Unpack[PublishHtmlDocTreeKwargs],
) -> str | None:
    """Return HTML from reStructuredText source string.

    Examples
    --------
    >>> html = publish_html_from_source("Hello **world**")
    >>> html is not None and "world" in html
    True
    """
    doctree = publish_doctree(source)
    return publish_html_from_doctree(doctree, **kwargs)


def publish_html_from_doctree(
    doctree: nodes.document,
    show_title: bool = True,
    toc_only: bool = False,
) -> str | None:
    """Return HTML from reStructuredText document (doctree).

    Parameters
    ----------
    doctree : docutils.nodes.document
        reStructuredText document (doctree) to render
    show_title : bool
        Show top level title
    toc_only : bool
        Special flag: return show TOC, used for sidebars

    Returns
    -------
    str or None
        HTML from reStructuredText document (doctree)

    Examples
    --------
    >>> doctree = publish_doctree("Hello **world**")
    >>> html = publish_html_from_doctree(doctree)
    >>> html is not None and "<strong>world</strong>" in html
    True
    """
    writer = DjangoDocutilsWriter()

    doctree.transformer.apply_transforms()

    if toc_only:  # special flag to only return toc, used for sidebars
        return publish_toc_from_doctree(doctree, writer=writer)

    parts = publish_parts_from_doctree(
        doctree,
        writer=writer,
    )

    if show_title:
        return mark_safe(force_str(parts["html_body"]))
    return mark_safe(force_str(parts["fragment"]))
