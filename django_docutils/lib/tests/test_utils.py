from django_docutils.lib.utils import chop_after_docinfo, chop_after_title


def test_chop_after_title():
    content = """=============================================
Learn JavaScript for free: The best resources
=============================================

first section
-------------

some content
""".strip()

    result = chop_after_title(content)

    expected = """
first section
-------------

some content""".strip()

    assert result == expected


def test_chop_after_docinfo():
    before = """
===========
Content ok!
===========

:programming_languages: javascript
:topics: webpack
:Created: 2017-07-30
:Author: tony

more text

first section
-------------

some content
""".strip()

    after = """
more text

first section
-------------

some content
""".strip()

    assert chop_after_docinfo(before) == after

    # test docinfo handles spaces in values
    assert (
        chop_after_docinfo(
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

hi
    """.strip()
        )
        == """
Content
-------

hi""".strip()
    )
