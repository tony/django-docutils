"""Docutils Publisher fors for Django Docutils."""
import typing as t

from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe
from docutils import io, nodes
from docutils.core import Publisher, publish_doctree as docutils_publish_doctree
from docutils.readers.doctree import Reader
from docutils.writers.html5_polyglot import Writer

from .directives.registry import register_django_docutils_directives
from .roles.registry import register_django_docutils_roles
from .settings import DJANGO_DOCUTILS_LIB_RST
from .transforms.toc import Contents
from .writers import DjangoDocutilsWriter

if t.TYPE_CHECKING:
    from docutils import SettingsSpec

docutils_settings = DJANGO_DOCUTILS_LIB_RST.get("docutils", {})


def publish_parts_from_doctree(
    document: nodes.document,
    destination_path: str | None = None,
    writer: Writer | None = None,
    writer_name: str = "pseudoxml",
    settings: t.Any | None = None,
    settings_spec: "SettingsSpec | None" = None,
    settings_overrides: t.Any | None = None,
    config_section: str | None = None,
    enable_exit_status: bool = False,
) -> t.Dict[str, str]:
    """Render docutils doctree into docutils parts."""
    reader = Reader(parser_name="null")
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
        settings_spec,  # type:ignore
        settings_overrides,
        config_section,  # type:ignore
    )
    pub.set_destination(None, destination_path)
    pub.publish(enable_exit_status=enable_exit_status)
    return pub.writer.parts  # type:ignore


def publish_toc_from_doctree(
    doctree: nodes.document,
    writer: Writer | None = None,
) -> t.Optional[str]:
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
    settings_overrides: t.Any = docutils_settings,
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
    """
    register_django_docutils_directives()
    register_django_docutils_roles()

    return docutils_publish_doctree(
        source=force_bytes(source),
        settings_overrides=settings_overrides,
    )


if t.TYPE_CHECKING:
    from typing_extensions import NotRequired, TypedDict, Unpack

    class PublishHtmlDocTreeKwargs(TypedDict):
        """Keyword arguments accepted by publish_html_from_source."""

        show_title: NotRequired[bool]
        toc_only: NotRequired[bool]


def publish_html_from_source(
    source: str,
    **kwargs: "Unpack[PublishHtmlDocTreeKwargs]",
) -> str | None:
    """Return HTML from reStructuredText source string."""
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
    value : str
        Contents from template being placed into node
    show_title : bool
        Show top level title
    toc_only : bool
        Special flag: return show TOC, used for sidebars

    Returns
    -------
    str or None
        HTML from reStructuredText document (doctree)
    """
    writer = DjangoDocutilsWriter()

    doctree.transformer.apply_transforms()

    if toc_only:  # special flag to only return toc, used for sidebars
        return publish_toc_from_doctree(doctree, writer=writer)

    parts = publish_parts_from_doctree(
        doctree,
        writer=writer,
        settings_overrides=docutils_settings,
    )

    if show_title:
        return mark_safe(force_str(parts["html_body"]))
    else:
        return mark_safe(force_str(parts["fragment"]))
