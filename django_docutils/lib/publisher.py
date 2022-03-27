from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe
from docutils import io, nodes, readers
from docutils.core import Publisher, publish_doctree as docutils_publish_doctree

from .directives import register_based_directives
from .roles import register_based_roles
from .settings import BASED_LIB_RST, INJECT_FONT_AWESOME
from .transforms.toc import Contents
from .writers import BasedWriter

docutils_settings = BASED_LIB_RST.get("docutils", {})


def publish_parts_from_doctree(
    document,
    destination_path=None,
    writer=None,
    writer_name="pseudoxml",
    settings=None,
    settings_spec=None,
    settings_overrides=None,
    config_section=None,
    enable_exit_status=False,
):
    reader = readers.doctree.Reader(parser_name="null")
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
    pub.process_programmatic_settings(settings_spec, settings_overrides, config_section)
    pub.set_destination(None, destination_path)
    pub.publish(enable_exit_status=enable_exit_status)
    return pub.writer.parts


def publish_toc_from_doctree(doctree, writer=None, pages=None, current_page=None):
    if not writer:
        writer = BasedWriter()
    # Create a new document tree with just the table of contents
    # ==========================================================

    # document tree template:
    toc_tree = nodes.document(
        "", "", source="toc-generator", classes=["fixed-toc-menu menu"]
    )
    toc_tree += nodes.paragraph("", "Contents", classes=["menu-label"])
    # Set up a Contents instance:
    # The Contents transform requires a "pending" startnode and
    # generation options startnode
    pending = nodes.pending(Contents, rawsource="")

    contents_transform = Contents(doctree, pending)

    # this assures we get backlinks pointing to themselves
    # so users can copy anchor from headers
    contents_transform.backlinks = "entry"

    toc_contents = contents_transform.build_contents(doctree)

    if not toc_contents:  # ToC is empty
        return None

    # run the contents builder and append the result to the template:
    toc_topic = nodes.topic(classes=["contents", "toc"])

    # if multi-page post, add page contents and inject into current page
    if pages and len(pages) > 1 and current_page:
        page_entries = []
        for page in pages:
            reference = nodes.reference(
                page.get_absolute_url(), page.subtitle, refuri=page.get_absolute_url()
            )
            item = nodes.list_item("", reference)
            if page == current_page:
                # make sure current page link is active
                reference["classes"] = ["is-active"]

                # append toc to the active page
                toc_contents["classes"].append("is-active")
                item += toc_contents
            # add the rest of te page entries
            page_entries.append(item)
        toc_topic += nodes.bullet_list("", *page_entries, classes=["menu-list"])
    else:
        toc_topic += toc_contents
    toc_tree += toc_topic
    toc = publish_parts_from_doctree(toc_tree, writer=writer)
    return mark_safe(force_str(toc["html_body"]))


def publish_doctree(source, settings_overrides=docutils_settings):
    """Split off ability to get doctree (a.k.a. document)

    It's valuable to be able to run transforms to alter and most importantly,
    extract data like post abstracts.

    :param source: RST content
    :type source: content
    :rtype: :class:`docutils.nodes.document`
    :returns: document/doctree for reStructuredText content
    """
    register_based_directives()
    register_based_roles()

    return docutils_publish_doctree(
        source=force_bytes(source), settings_overrides=settings_overrides
    )


def publish_html_from_source(source, *args, **kwargs):
    """Return HTML from reStructuredText source string."""

    doctree = publish_doctree(source)
    return publish_html_from_doctree(doctree, *args, **kwargs)


def publish_html_from_doctree(
    doctree,
    show_title=True,
    toc_only=False,
    inject_ads=False,
    ad_keywords=[],
    pages=[],
    current_page=None,
):
    """Return HTML from reStructuredText document (doctree).

    :param value: Contents from template being placed into node
    :type value: string
    :param show_title: show top level ittle
    :type show_title: bool
    :param toc_only: special flag: return show TOC, used for sidebars
    :type toc_only: bool
    :param ad_keywords: keywords to send to backend to serve targetted ads
    :type ad_keywords: list of strings
    :param pages: optional list of pages, if multi-page post
    :type pages: :class:`~django:django.db.models.query.QuerySet`
    :param current_page: current page (only applicable if pages)
    :type current_page: :class:`django:django.db.models.Model
    """

    writer = BasedWriter()

    if inject_ads:
        from django_docutils.lib.transforms.ads import InjectAds

        doctree.transformer.add_transform(InjectAds.keywords(ad_keywords))

    if INJECT_FONT_AWESOME:
        from django_docutils.lib.transforms.font_awesome import InjectFontAwesome

        doctree.transformer.add_transform(InjectFontAwesome)

    doctree.transformer.apply_transforms()

    if toc_only:  # special flag to only return toc, used for sidebars
        return publish_toc_from_doctree(
            doctree, writer=writer, pages=pages, current_page=current_page
        )

    parts = publish_parts_from_doctree(
        doctree, writer=writer, settings_overrides=docutils_settings
    )

    if show_title:
        return mark_safe(force_str(parts["html_body"]))
    else:
        return mark_safe(force_str(parts["fragment"]))
