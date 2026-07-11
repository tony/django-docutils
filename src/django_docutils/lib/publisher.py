"""Docutils Publisher fors for Django Docutils."""

from __future__ import annotations

import typing as t

from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe
from docutils import io, nodes
from docutils.core import Publisher, publish_doctree as docutils_publish_doctree
from docutils.readers.doctree import Reader

from .directives.registry import register_django_docutils_directives
from .roles.registry import register_django_docutils_roles
from .sanitize import sanitize_doctree
from .settings import get_docutils_settings
from .transforms.toc import Contents
from .writers import DjangoDocutilsWriter

if t.TYPE_CHECKING:
    from typing_extensions import NotRequired, Unpack


def publish_parts_from_doctree(
    document: nodes.document,
    destination_path: str | None = None,
    writer: t.Any | None = None,
    writer_name: str = "pseudoxml",
    settings: t.Any | None = None,
    settings_spec: t.Any | None = None,
    settings_overrides: t.Mapping[str, object] | None = None,
    config_section: str | None = None,
    enable_exit_status: bool = False,
) -> dict[str, str]:
    """Render docutils doctree into docutils parts.

    Parameters
    ----------
    document : docutils.nodes.document
        Doctree to sanitize and render.
    destination_path : str, optional
        Destination path handed to the docutils publisher.
    writer : docutils.writers.Writer, optional
        Writer instance; ``writer_name`` selects one when omitted.
    writer_name : str
        Writer name used when ``writer`` is not given.
    settings : optional
        Pre-built docutils settings object. The resolved security settings
        are written onto it, but configuration files it already read cannot
        be retroactively undone — prefer ``None``.
    settings_spec : optional
        docutils settings spec passed through to the publisher.
    settings_overrides : mapping, optional
        Per-call Docutils settings resolved via
        :func:`~django_docutils.lib.settings.get_docutils_settings`.
    config_section : str, optional
        docutils configuration section passed through to the publisher.
    enable_exit_status : bool
        Forwarded to ``Publisher.publish``.

    Returns
    -------
    dict
        docutils parts (e.g. ``html_body``) keyed by part name.

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

    # Reuse the resolved settings for the writer's final sanitize pass so it
    # applies the same policy as the pre-publish pass above (e.g. a per-call
    # raw_enabled override under the project opt-in).
    if writer is not None:
        writer.django_docutils_settings = docutils_settings

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
    writer: t.Any | None = None,
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


class PublishHtmlDocTreeKwargs(t.TypedDict):
    """Keyword arguments accepted by publish_html_from_source."""

    show_title: NotRequired[bool]
    toc_only: NotRequired[bool]


def publish_html_from_source(
    source: str,
    **kwargs: Unpack[PublishHtmlDocTreeKwargs],
) -> str | None:
    """Return HTML from reStructuredText source string.

    Parameters
    ----------
    source : str
        reStructuredText content.
    **kwargs : PublishHtmlDocTreeKwargs
        Rendering flags forwarded to :func:`publish_html_from_doctree`.

    Returns
    -------
    str or None
        Rendered HTML, or ``None`` when only an empty TOC was requested.

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
