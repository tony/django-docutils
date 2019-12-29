import pytest

import responses

from django_docutils.exc import BasedException
from django_docutils.favicon.scrape import _request_favicon, get_favicon


@responses.activate
def test__request_favicon_rejects_wrong_type():
    url = 'https://aklsdfjaweof.com'

    # page response
    responses.add(responses.GET, url, body='blah', status=200, content_type='text/html')

    with pytest.raises(BasedException, match=r'Not an image'):
        _request_favicon(url)


@responses.activate
def test_get_favicon_url_connection():
    url = 'https://aklsdfjaweof.com'

    with pytest.raises(BasedException, match=r'The website .* isn\'t connecting.'):
        get_favicon(url)


@responses.activate
def test_get_favicon_url_catches_shortcut_icon():
    url = 'https://aklsdfjaweof.com'
    favicon_url = f'{url}/images/favicon.ico'
    favicon_content = b'lol'

    responses.add(
        responses.GET,
        url,
        body='<link rel="shortcut icon" href="{favicon_url}" />'.format(
            favicon_url=favicon_url
        ),
        status=200,
        content_type='text/html',
    )

    responses.add(
        responses.GET,
        favicon_url,
        body=favicon_content,
        status=200,
        content_type='image/ico',
    )

    assert get_favicon(url) == favicon_content


@responses.activate
def test_get_favicon_url_falls_back_to_root_favicon_error_retrieve():
    """In this case, pattern exists, but favicon URL in pattern bad.

    The get_faviconr should then attempt to connect to site_root/favicon.ico"""
    url = 'https://aklsdfjaweof.com'
    favicon_url = f'{url}/images/favicon.ico'
    root_favicon_url = f'{url}/favicon.ico'
    favicon_content = b'lol'

    responses.add(
        responses.GET,
        url,
        body='<link rel="shortcut icon" href="{favicon_url}" />'.format(
            favicon_url=favicon_url
        ),
        status=200,
        content_type='text/html',
    )

    responses.add(
        responses.GET,
        root_favicon_url,
        body=favicon_content,
        status=200,
        content_type='image/ico',
    )

    assert get_favicon(url) == favicon_content


@responses.activate
def test_get_favicon_url_falls_back_to_root_favicon_no_pattern():
    """In this case, page loads, but 'shortcut icon' pattern not found.

    The get_faviconr should then attempt to connect to site_root/favicon.ico"""
    url = 'https://aklsdfjaweof.com'
    favicon_url = f'{url}/images/favicon.ico'
    root_favicon_url = f'{url}/favicon.ico'
    favicon_content = b'lol'

    responses.add(
        responses.GET,
        url,
        body=f'<link rel="nope" href="{favicon_url}" />',
        status=200,
        content_type='text/html',
    )

    responses.add(
        responses.GET,
        root_favicon_url,
        body=favicon_content,
        status=200,
        content_type='image/ico',
    )

    assert get_favicon(url) == favicon_content


@responses.activate
def test_get_favicon_raises_exception_all_strategies_fail():
    """Raise BasedException if none of the favicon download methods work."""
    url = 'https://aklsdfjaweof.com'

    # page response
    responses.add(responses.GET, url, body='blah', status=200, content_type='text/html')

    with pytest.raises(BasedException, match=r'Could not retrieve favicon for .*'):
        assert get_favicon(url)
