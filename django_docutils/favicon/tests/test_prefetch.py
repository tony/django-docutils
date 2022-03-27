import pytest

import responses
from django.core.files.uploadedfile import SimpleUploadedFile
from docutils.nodes import document
from inmemorystorage.storage import InMemoryFile

from django_docutils.favicon.prefetch import (
    is_favicon_stored,
    prefetch_favicon,
    yield_page_doctrees,
    yield_references,
)
from django_docutils.lib.publisher import publish_doctree

TEST_RST_DOCUMENT = """
Developing
==========

- Make a hobby website in django or flask.

  Services like `Heroku`_ are free to try, and simple to deploy Django
  websites to.

- For free editors, check out good old `vim`_, `Visual Studio Code`_,
  `Atom`_, or `PyCharm`_

.. _Visual Studio Code: https://code.visualstudio.com/
.. _Atom: https://atom.io/
.. _vim: http://vim.org
.. _PyCharm: https://www.jetbrains.com/pycharm/
"""


def test_yield_references():
    document = publish_doctree(TEST_RST_DOCUMENT)
    assert set(yield_references(document)) == {
        "https://code.visualstudio.com/",
        "https://atom.io/",
        "http://vim.org",
        "https://www.jetbrains.com/pycharm/",
    }


def test_yield_references_patterns():
    document = publish_doctree(TEST_RST_DOCUMENT)
    assert set(yield_references(document, url_pattern="atom")) == {"https://atom.io/"}


@pytest.mark.django_db(transaction=True)
def test_yield_page_doctrees(RSTPostPage):
    RSTPostPage.objects.create(subtitle="lol", body=TEST_RST_DOCUMENT)
    assert RSTPostPage.objects.filter(subtitle="lol").count()

    page_doctrees = list(yield_page_doctrees(RSTPostPage))
    assert len(page_doctrees)

    for page in page_doctrees:
        assert isinstance(page, document)


@pytest.mark.django_db(transaction=True)
@responses.activate
def test_prefetch_favicon_working():
    url = "http://vim.org"
    favicon_url = f"{url}/images/favicon.ico"
    favicon_content = b"lol"

    responses.add(
        responses.GET,
        url,
        body='<link rel="shortcut icon" href="{favicon_url}" />'.format(
            favicon_url=favicon_url
        ),
        status=200,
        content_type="text/html",
    )

    responses.add(
        responses.GET,
        favicon_url,
        body=favicon_content,
        status=200,
        content_type="image/ico",
    )

    favicon, created = prefetch_favicon(url)

    assert favicon.favicon.read() == favicon_content


@pytest.mark.django_db(transaction=True)
@responses.activate
def test_prefetch_favicon_file_missing(monkeypatch):
    # case where the favicon is in ORM, but file not in storage
    url = "http://vim.org"
    favicon_url = f"{url}/images/favicon.ico"
    favicon_content = b"lol"

    responses.add(
        responses.GET,
        url,
        body='<link rel="shortcut icon" href="{favicon_url}" />'.format(
            favicon_url=favicon_url
        ),
        status=200,
        content_type="text/html",
    )

    responses.add(
        responses.GET,
        favicon_url,
        body=favicon_content,
        status=200,
        content_type="image/ico",
    )

    def mock_file():
        raise FileNotFoundError

    favicon, created = prefetch_favicon(url)

    import django_docutils.favicon.prefetch

    assert not prefetch_favicon(url)
    monkeypatch.setattr(
        django_docutils.favicon.prefetch, "is_favicon_stored", lambda fqdn: False
    )

    favicon, created = prefetch_favicon(url)
    assert not created


@pytest.mark.django_db(transaction=True)
@responses.activate
def test_is_favicon_stored_file_missing(monkeypatch, Favicon):
    # case where the favicon is in ORM, but file not in storage
    url = "http://vim.org"
    fqdn = "vim.org"

    def mock_open(path, mode="r"):
        raise FileNotFoundError

    favicon = Favicon.objects.create(
        domain=fqdn,
        favicon=SimpleUploadedFile(
            name=f"{fqdn}.ico",
            content=b"lol",
            content_type="image/ico",
        ),
    )

    assert not prefetch_favicon(url), "File should not redownload"

    monkeypatch.setattr(InMemoryFile, "open", mock_open)
    with pytest.raises(FileNotFoundError):  # Assure monkeypatch
        favicon.favicon.file

    assert not is_favicon_stored(
        favicon.domain
    ), "favicon missing from storage should return False"


@pytest.mark.django_db(transaction=True)
@responses.activate
def test_is_favicon_stored_favicon_not_in_db(monkeypatch):
    assert not is_favicon_stored(
        "nonexistant_fqdn.com"
    ), "favicon missing from database should return False"
