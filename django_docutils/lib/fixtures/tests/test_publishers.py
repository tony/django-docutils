import pytest

from django.conf import settings

from django_docutils.lib.fixtures.publisher import publish_post


@pytest.mark.django_db(transaction=True)
def test_publish_post_from_source_file(tmpdir):
    test_file = tmpdir.join("test.rst")
    test_file.write(
        """
===
moo
===

:Author: anonymous
:Slug_Id: tEst

foo
    """.strip()
    )
    post_data = publish_post(source_path=str(test_file))
    assert isinstance(post_data, dict)


@pytest.mark.django_db(transaction=True)
def test_publish_post_explicitness():
    """If title, subtitle, created, updated, etc. is declared in metadata,
    that is treated as a source of truth, and the database entry must
    respect that, upon initial import and subsequent re-imports.

    @todo a test also needs to be made for this and the directory style
    configurations.
    @todo parametrize this with message, source, results
    """

    assert publish_post(source="") == {}

    # test with title
    assert (
        publish_post(
            source="""
==============
Document title
==============
    """.strip()
        )
        == {"title": "Document title"}
    )

    # test with subtitle
    assert (
        publish_post(
            source="""
==============
Document title
==============
-----------------
Document subtitle
-----------------
    """.strip()
        )
        == {"title": "Document title", "pages": [{"subtitle": "Document subtitle"}]}
    )

    # test with content
    assert (
        publish_post(
            source="""
==============
Document title
==============
-----------------
Document subtitle
-----------------

Content
-------

hi
    """.strip()
        )
        == {
            "title": "Document title",
            "pages": [
                {
                    "subtitle": "Document subtitle",
                    "body": """
Content
-------

hi""".strip(),
                }
            ],
        }
    )

    # assert with header content
    assert (
        publish_post(
            source="""
==============
Document title
==============
-----------------
Document subtitle
-----------------

Content
-------

hi1
    """.strip()
        )
        == {
            "title": "Document title",
            "pages": [
                {
                    "subtitle": "Document subtitle",
                    "body": """
Content
-------

hi1""".strip(),
                }
            ],
        }
    )

    # assert with basic docinfo
    assert (
        publish_post(
            source="""
==============
Document title
==============
-----------------
Document subtitle
-----------------

:Author: anonymous
:Slug_Id: tEst

Content
-------

hi2
    """.strip()
        )
        == {
            "title": "Document title",
            "author": settings.ANONYMOUS_USER_NAME,
            "slug_id": "tEst",
            "pages": [
                {
                    "subtitle": "Document subtitle",
                    "body": """
Content
-------

hi2""".strip(),
                }
            ],
        }
    )

    # assert with title/subtitle docinfo override
    assert (
        publish_post(
            source="""
==============
Document title
==============
-----------------
Document subtitle
-----------------

:Title: Overridden Title
:Subtitle: Overridden Subtitle

Content
-------

moo
    """.strip()
        )
        == {
            "title": "Overridden Title",
            "pages": [
                {
                    "subtitle": "Overridden Subtitle",
                    "body": """
Content
-------

moo""".strip(),
                }
            ],
        }
    )

    # assert with title/subtitle docinfo override + new fields
    assert (
        publish_post(
            source="""
==============
Document title
==============
-----------------
Document subtitle
-----------------

:Title: Overridden Title
:Subtitle: Overridden Subtitle
:Slug_Id: tEst

Content
-------

hi
    """.strip()
        )
        == {
            "title": "Overridden Title",
            "slug_id": "tEst",
            "pages": [
                {
                    "subtitle": "Overridden Subtitle",
                    "body": """
Content
-------

hi""".strip(),
                }
            ],
        }
    )


def test_publish_post_defaults():
    # default value pass-through
    assert publish_post(
        source="", defaults={"moo": "moo", "title": "default title"}
    ) == {"moo": "moo", "title": "default title"}

    # title and subtitle from doc override defaults
    assert (
        publish_post(
            source="""
==============
Document title
==============
-----------------
Document subtitle
-----------------
    """.strip(),
            defaults={"moo": "moo"},
        )
        == {
            "title": "Document title",
            "moo": "moo",
            "pages": [{"subtitle": "Document subtitle"}],
        }
    )

    # Docinfo overrides doc nodes and defaults
    assert (
        publish_post(
            source="""
==============
Document title
==============
-----------------
Document subtitle
-----------------

:Title: Overridden Title
:Subtitle: Overridden Subtitle
:Slug_Id: tEst

Content
-------

hi
    """.strip(),
            defaults={
                "title": "You should not",
                "subtitle": "See this",
                "a_default_property": "a_default_value",
            },
        )
        == {
            "title": "Overridden Title",
            "slug_id": "tEst",
            "a_default_property": "a_default_value",
            "pages": [
                {
                    "subtitle": "Overridden Subtitle",
                    "body": """
Content
-------

hi""".strip(),
                }
            ],
        }
    )


def test_publish_post_overrides():
    # default value pass-through
    assert publish_post(source="", overrides={"moo": "moo"}) == {"moo": "moo"}

    # override defaults
    assert publish_post(
        source="",
        defaults={"moo": "moo", "title": "default title"},
        overrides={"moo": "moo2"},
    ) == {"moo": "moo2", "title": "default title"}

    # override overrides doc title/subtitle
    assert (
        publish_post(
            source="""
==============
Document title
==============
-----------------
Document subtitle
-----------------
    """.strip(),
            overrides={"title": "Over", "subtitle": "Written"},
        )
        == {"title": "Over", "pages": [{"subtitle": "Written"}]}
    )

    # overrides overrides docinfo
    assert (
        publish_post(
            source="""
==============
Document title
==============
-----------------
Document subtitle
-----------------

:Title: Overridden Title
:Subtitle: Overridden Subtitle
:Slug_Id: tEst

Content
-------

hi
    """.strip(),
            overrides={
                "title": "You should",
                "subtitle": "See this",
                "slug_id": "and this",
                "a_default_property": "a_default_value",
            },
        )
        == {
            "title": "You should",
            "slug_id": "and this",
            "a_default_property": "a_default_value",
            "pages": [
                {
                    "subtitle": "See this",
                    "body": """
Content
-------

hi""".strip(),
                }
            ],
        }
    )
