"""Extract post and page data from reStructuredText.

publish_post
------------

Posts contain pages. Since posts contain multiple page support out of the box,
both the source and source_path property accept on value or a list of values.

publish_page
------------

This is a low-level, single-file publisher used by publish_post. It's made
available to keep the functions *somewhat* pure and abstract away the
m2m connections publish_post builds. It's also made available to make tests
simpler.

How page/post properties are resolved
-------------------------------------

These publishers not only process reStructuredText, but extract important
information needed by the Post models.

Since in some cases the page/post properties may be injected from other
sources, such as a manifest.json file in directories, there are options
to pass in a default and override dictionary of properties.

FYI: 'body' is the content of the reStructuredText after the title/subtitle
and docinfo.

There are rules in which data takes precedence / cascades:

1. Default data: fill any post properties in by default. this can be any
   k/v that the post can return, such as title, subtitle, created,
   updated, topics, etc.
2. The title/subtitle are picked from the source, if exists::

        =====
        Title
        =====
        --------
        Subtitle
        --------

    Data::

        {
            'title': 'Title'
            'subtitle': 'Subtitle'
        }
3. docinfo (http://docutils.sourceforge.net/docs/ref/doctree.html#docinfo)
   is merged into the data.

   If a title or subtitle is mentioned in it, it takes precendence over
   the documement node title/subtitle. For instance::

        =====
        Title
        =====
        -------- Subtitle --------

        :Title: My Title
        :Subtitle: My Subtitle

   Data::

        {
            'title': 'My Title'
            'subtitle': 'My Subtitle'
        }
4. Any override values are merged on top, so assuming the last example,
   if::

        overrides = {
            'title': 'Overridden title'
        }

   Data::

        {
            'title': 'Overridden title',
            'subtitle'; 'My Subtitle'
        }

"""
from django.utils.encoding import force_bytes

from django_docutils.lib.metadata.extract import (
    extract_metadata,
    extract_subtitle,
    extract_title,
)
from django_docutils.lib.metadata.process import process_metadata
from django_docutils.lib.utils import chop_after_heading_smartly

from ..publisher import publish_doctree
from ..settings import BASED_LIB_RST
from .utils import split_page_data

docutils_settings = BASED_LIB_RST.get("docutils", {})

#: post fields with m2m relations
M2M_FIELDS = ["programming_languages", "topics", "platforms", "series"]

#: fields that overwrite manual values
AUTO_FIELDS = ["created", "modified", "slug_title"]


def publish_post(source=None, source_path=None, defaults={}, overrides={}):
    """Returns processed data from RST source, for DB insertion.

    The dict returned should nearly resemble a Post model.

    :param source: source
    :type source: str or list
    :param source_path: path to a source file
    :type source_path: str or list
    ;param defaults: default document information to seed, can be overwritten
         by docinfo attributes, title, subitle, in the RST source.
    :type defaults: dict
    ;param overrides: document information that persists, even if docinfo
    :type overrides: dict
    :returns: dict of params (nearly-)ready for ORM insertion
    :rtype: dict

    """

    pages = []  # all posts contain one or more pages inside

    if source is not None:
        if isinstance(source, str):
            sources = [source]
        elif isinstance(source, list):
            sources = source
    elif source_path:
        if isinstance(source_path, str):
            sources = [open(source_path).read()]
        elif isinstance(source_path, list):
            sources = [open(spath).read() for spath in source_path]

    for source in sources:
        page_data = publish_page(source=source, defaults=defaults, overrides=overrides)

        # done, now split out page related data
        post_data, page_data = split_page_data(page_data)
        # append page data, and then move to next source / page
        if page_data:
            pages.append(page_data)

    if pages:
        post_data["pages"] = pages
    return post_data


def publish_page(source=None, source_path=None, defaults={}, overrides={}):
    """Publish a restructured text source or file, return metadata.

    :param source: source
    :type source: str or list
    :param source_path: path to a source file
    :type source_path: str or list
    ;param defaults: default document information to seed, can be overwritten
         by docinfo attributes, title, subitle, in the RST source.
    :type defaults: dict
    ;param overrides: document information that persists, even if docinfo
    :type overrides: dict
    """
    if source_path:
        source = open(source_path).read()

    doctree = publish_doctree(
        source=force_bytes(source), settings_overrides=docutils_settings
    )

    # Step 0: fresh data dict
    page_data = {}

    # Step 1. start with the default
    page_data.update(defaults)

    # Step 2: pluck document node-related attributes from document
    document_data = {}
    try:
        document_data["body"] = chop_after_heading_smartly(source)
    except IndexError:
        pass
    document_data["title"] = extract_title(doctree)
    document_data["subtitle"] = extract_subtitle(doctree)

    # clean empty values
    document_data = {k: v for k, v in document_data.items() if v}

    # merge document node-related data
    page_data.update(document_data)

    # Step 3: override node-related document attributes
    docinfo = process_metadata(extract_metadata(doctree))
    page_data.update(docinfo)

    # override with any override explicit data
    page_data.update(overrides)

    return page_data
