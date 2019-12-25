#!/usr/bin/env python
import logging
import sys
from urllib.parse import urljoin

import requests
from lxml import html
from six.moves.urllib.parse import urlparse

from django_docutils.exc import BasedException

logger = logging.getLogger(__name__)


def _request_favicon(url):
    """Tries to download favicon from URL and checks if it's valid."""
    r = requests.get(url)
    r.raise_for_status()
    if 'image' not in r.headers['Content-Type']:
        raise BasedException('Not an image')
    return r.content


def get_favicon(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        # update url if redirected
        if r.url != url:
            url = r.url
        doc = html.fromstring(r.content)
    except requests.exceptions.ConnectionError as e:
        raise BasedException(f"The website {url} isn't connecting:", e)

    paths = ['//link[@rel="shortcut icon"]/@href', '//link[@rel="icon"]/@href']
    for path in paths:
        # Method 1: to find favicon via "shortcut icon"
        favicons = doc.xpath(path)

        if len(favicons):  # Is pattern found?
            try:
                favicon_url = favicons[0]
                favicon_url = urljoin(url, favicon_url)
                return _request_favicon(favicon_url)
            except Exception as e:
                logger.debug(
                    'Could not retrieve {favicon_url}: \n{e}'.format(
                        favicon_url=favicon_url, e=e
                    )
                )

    # Method 2: site root/favicon.ico
    try:
        parsed = urlparse(url)
        parsed = parsed._replace(path='/favicon.ico')
        favicon_url = parsed.geturl()
        return _request_favicon(favicon_url)
    except Exception as e:
        logger.debug(
            'Could not retrieve {favicon_url}.\n{e}'.format(
                favicon_url=favicon_url, e=e
            )
        )

    raise BasedException(
        """
Could not retrieve favicon for {url}. Both strategies failed
        """.format(
            url=url
        )
    )


if __name__ == '__main__':
    favicon = get_favicon(sys.argv[1])
    file_ = open('/Users/me/favicon.ico', 'wb')
    file_.write(favicon)
    file_.close()
