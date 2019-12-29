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
import os

from django.contrib.auth import get_user_model
from django_slugify_processor.text import slugify

from django_docutils.lib.fixtures.directory.extract import extract_dir_config
from django_docutils.lib.fixtures.directory.utils import (
    find_rst_dirs_in_app,
    find_series_files,
)
from django_docutils.lib.fixtures.publisher import M2M_FIELDS, publish_post
from django_docutils.lib.fixtures.utils import (
    find_rst_files_in_app,
    get_model_from_post_app,
    split_page_data,
)
from django_docutils.lib.metadata.process import process_metadata
from django_docutils.lib.settings import BASED_LIB_RST

docutils_settings = BASED_LIB_RST.get('docutils', {})

User = get_user_model()


def split_m2m_metadata(metadata):
    """Split the m2m_fields from the metadata

    Pluck out m2m relations and put them into m2m_metadata
    because they can't be placed into model w/o it being saved
    """
    m2m_metadata = {}
    for k, v in metadata.items():
        if k in M2M_FIELDS:
            m2m_metadata[k] = metadata[k]
    metadata = {key: val for key, val in metadata.items() if key not in M2M_FIELDS}
    return m2m_metadata, metadata


def load_post_data(model, metadata):  # NOQA: C901
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

    metadata['author_name'] = metadata.pop('author', 'Anonymous')

    pages = metadata.pop('pages')

    m, created = model.objects.update_or_create(
        slug_id=metadata['slug_id'], defaults=metadata
    )

    # assure metadata fields stick with auto-generated fields
    for field in ['created', 'modified', 'slug_title']:
        if field in metadata:
            if getattr(m, field) != metadata[field]:
                setattr(m, field, metadata[field])

    # assure slugs update if title different (if not manually overwridden)
    # todo, only run this if title changed
    if not created and m.title and 'slug_title' not in metadata:
        m.slug_title = slugify(m.title)

    if m.is_dirty():
        m.save()

    for page in m.pages.all():  # we can safely delete and re-add content
        page.delete()

    PostPage = m.pages.model

    # re-add one-to-many post -> page associations
    for page_number, page_data in enumerate(pages, 1):
        _, post_page = split_page_data(page_data)
        post_page['page_number'] = page_number

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


def load_app_rst_fixtures(app_config, model=None):
    """Load fixtures projects (single and dir) into ORM.

    High-level function that detects and handles both types of files.

    :param app_config: Configuration for django app
    :type app_config: :class:`django.apps.AppConfig`
    :param model: Model class, any polymorphic sub-class of
        django_docutils.rst_post.models.RSTPost

        Entirely optional, only used for test cases so far.:w
    :type model: :class:`django:django.db.models.Model`
    """
    posts = []

    if not model:
        model = get_model_from_post_app(app_config)  # load the app model

    rst_files = [  # load single-file posts
        os.path.join(app_config.path, 'fixtures', f)
        for f in find_rst_files_in_app(app_config)
    ]
    dir_projects = [  # load directory-style posts (potentially multiple posts)
        os.path.join(app_config.path, 'fixtures', d)
        for d in find_rst_dirs_in_app(app_config)
    ]

    for f in rst_files:
        post_data = publish_post(source_path=f)
        m = load_post_data(model, post_data)

        posts.append(m)

    for _dir in dir_projects:
        # for directories, the manifest.json is our docinfo ^_^
        docinfo = process_metadata(extract_dir_config(_dir))
        files = [os.path.join(_dir, f) for f in find_series_files(docinfo, _dir)]

        docinfo.pop('series', None)  # pop off the series order

        post_data = publish_post(source_path=files, defaults=docinfo)
        m = load_post_data(model, post_data)
        posts.append(m)

    return posts
