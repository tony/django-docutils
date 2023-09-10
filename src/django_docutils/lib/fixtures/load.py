"""There are two types of projects: single RST files and directory "dir".

Both reside in the fixtures/ folder of a django application.

1. Single RST files keep metadata at the top of the document
2. Directory projects can be multiple RST files, configs reside in
   *manifest.json* within the project directory.

The highest level piece of information required is the django app config:

- The django app config contains the path of an app, which is used to check
  for the presence of RST files to load.
- The django app config also contains the model. The model is found deducing
  which model is a Python subclass of posts.Post.

In addition, both ultimately store Post's. The only difference is "dir"
style projects can have multiple files, creating a series. This is what allows
based to create multi-page posts.

The information for series-related data is in the "Series" key of the
*manifest.json*. These are a list of files relative to the directory of the
"project.

"""
from django_slugify_processor.text import slugify

from django_docutils.lib.fixtures.publisher import M2M_FIELDS
from django_docutils.lib.fixtures.utils import (
    split_page_data,
)
from django_docutils.lib.settings import BASED_LIB_RST

docutils_settings = BASED_LIB_RST.get("docutils", {})


def split_m2m_metadata(metadata):
    """Split the m2m_fields from the metadata

    Pluck out m2m relations and put them into m2m_metadata
    because they can't be placed into model w/o it being saved
    """
    m2m_metadata = {}
    for k in metadata:
        if k in M2M_FIELDS:
            m2m_metadata[k] = metadata[k]
    metadata = {key: val for key, val in metadata.items() if key not in M2M_FIELDS}
    return m2m_metadata, metadata


def load_post_data(model, metadata):
    """Fully load metadata and contents into objects (including m2m relations)

    :param model: Model class, any polymorphic sub-class of
        django_docutils.rst_post.models.RSTPost
    :type model: :class:`django:django.db.models.Model`
    :param metadata:
    :type metadata: dict
    :returns: Instance of model
    """

    m2m_metadata, metadata = split_m2m_metadata(metadata)

    # try:
    #     metadata['author'] = User.objects.get(username=metadata['author'])
    # except (User.DoesNotExist, ProgrammingError):
    #     metadata['author'] = None

    metadata["author_name"] = metadata.pop("author", "Anonymous")

    pages = metadata.pop("pages")

    m, created = model.objects.update_or_create(
        slug_id=metadata["slug_id"], defaults=metadata
    )

    # assure metadata fields stick with auto-generated fields
    for field in ["created", "modified", "slug_title"]:
        if field in metadata and getattr(m, field) != metadata[field]:
            setattr(m, field, metadata[field])

    # assure slugs update if title different (if not manually overwridden)
    # todo, only run this if title changed
    if not created and m.title and "slug_title" not in metadata:
        m.slug_title = slugify(m.title)

    if m.is_dirty():
        m.save()

    for page in m.pages.all():  # we can safely delete and re-add content
        page.delete()

    PostPage = m.pages.model

    # re-add one-to-many post -> page associations
    for page_number, page_data in enumerate(pages, 1):
        _, post_page = split_page_data(page_data)
        post_page["page_number"] = page_number

        p = PostPage(**post_page)
        p.save()
        if page_number == 1:
            m.root_page = p
            m.save()

        m.pages.add(p)

    # memorize/cache subtitle from first page in Post model
    if m.pages.first().subtitle and m.subtitle != m.pages.first().subtitle:
        m.subtitle = m.pages.first().subtitle
        m.save()

    return m
