import datetime

import pytest

import pytz
from django.conf import settings

from django_docutils.lib.fixtures.load import load_app_rst_fixtures, load_post_data
from django_docutils.lib.fixtures.publisher import publish_post


@pytest.mark.django_db(transaction=True)
def test_load_post_explicitness_persists(bare_app_config, RSTPost):
    sample_page_body = """
==============
Document title
==============
-----------------
Document subtitle
-----------------

:Slug_Id: tEst
:Author: anonymous

Content
-------

hi
    """.strip()

    post_data = publish_post(sample_page_body)

    # assert default behavior
    post = load_post_data(RSTPost, post_data)

    assert post.title == 'Document title'
    assert post.pages.first().subtitle == 'Document subtitle'
    assert post.slug_id == 'tEst'


@pytest.mark.django_db(transaction=True)
def test_correct_date_on_initial_and_reimport(RSTPost):
    # check tests
    sample_page_body = """
==============
Document title
==============
-----------------
Document subtitle
-----------------

:Slug_Id: tEst2
:Author: anonymous
:created: 2017-01-25

Content
-------

hi
    """.strip()

    post_data = publish_post(sample_page_body)

    assert post_data['created'].year == 2017
    assert post_data['created'].month == 1
    assert post_data['created'].day == 25

    # assert default behavior
    post = load_post_data(RSTPost, post_data)

    assert post.created.year == 2017
    assert post.created.month == 1
    assert post.created.day == 25

    # simulate re-import
    post = load_post_data(RSTPost, post_data)

    assert post.created.year == 2017
    assert post.created.month == 1
    assert post.created.day == 25

    now = datetime.datetime.now(pytz.timezone('UTC'))

    assert post.modified.year == now.year
    assert post.modified.month == now.month
    assert post.modified.day == now.day


@pytest.mark.django_db(transaction=True)
def test_correct_slug_title_on_initial_and_reimport(RSTPost):
    slug_title = 'my_brief_url'
    sample_page_body = """
==============
Document title
==============
-----------------
Document subtitle
-----------------

:Slug_Id: tEst2
:Slug_title: {slug_title}
:Author: anonymous
:created: 2017-01-25

Content
-------

hi
    """.format(
        slug_title=slug_title
    ).strip()

    post_data = publish_post(sample_page_body)

    assert post_data['slug_title'] == slug_title

    # assert default behavior
    post = load_post_data(RSTPost, post_data)

    assert post.slug_title == slug_title

    # simulate re-import
    post = load_post_data(RSTPost, post_data)

    assert post.slug_title == slug_title


@pytest.mark.django_db(transaction=True)
def test_slug_title_updates_on_reimport(RSTPost):
    sample_page_body = """
==============
Document title
==============
-----------------
Document subtitle
-----------------

:Slug_Id: tEst2
:Author: anonymous
:created: 2017-01-25

Content
-------

hi
    """.strip()
    from django_slugify_processor.text import slugify

    post_data = publish_post(sample_page_body)

    # assert default behavior
    post = load_post_data(RSTPost, post_data)
    assert post.slug_title == slugify(post_data['title'])

    # simulate re-import with updated title
    new_title = 'a new title yay'
    new_slug_title = slugify(new_title)
    post_data['title'] = new_title
    post = load_post_data(RSTPost, post_data)

    assert post.slug_title == new_slug_title


@pytest.mark.django_db(transaction=True)
def test_load_app_rst_fixtures_minimal(sample_app_config, RSTPost):
    load_app_rst_fixtures(sample_app_config, model=RSTPost)


@pytest.mark.django_db(transaction=True)
def test_load_post_data_minimal(RSTPost):
    pages = [{'body': 'moo', 'subtitle': 'my subtitle'}]

    post = load_post_data(
        RSTPost,
        {'author': settings.ANONYMOUS_USER_NAME, 'slug_id': 'aFeuM8e', 'pages': pages},
    )

    assert isinstance(post, RSTPost)
