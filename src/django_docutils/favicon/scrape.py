#!/usr/bin/env python
import logging
import sys
from urllib.parse import urljoin, urlparse

import requests
from lxml import html

from django_docutils.exc import BasedException

logger = logging.getLogger(__name__)


class FaviconNotImageError(BasedException):
    def __init__(self, *args: object, **kwargs):
        return super().__init__(
            "Not an image",
            *args,
            **kwargs,
        )


def _request_favicon(url):
    """Tries to download favicon from URL and checks if it's valid."""
    r = requests.get(url)
    r.raise_for_status()
    if "image" not in r.headers["Content-Type"]:
        raise FaviconNotImageError()
    return r.content


class FaviconURLConnectionError(BasedException, requests.exceptions.ConnectionError):
    def __init__(self, url: str, *args: object, **kwargs):
        return super().__init__(
            f"The website {url} isn't connecting.",
            *args,
            **kwargs,
        )


class FaviconURLRetrievalFailed(BasedException):
    def __init__(self, url: str, *args: object, **kwargs):
        return super().__init__(
            f"Could not retrieve favicon for {url}. Both strategies failed",
            *args,
            **kwargs,
        )


def get_favicon(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        # update url if redirected
        if r.url != url:
            url = r.url
        doc = html.fromstring(r.content)
    except requests.exceptions.ConnectionError as e:
        raise FaviconURLConnectionError(url=url) from e

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
                logger.debug(f"Could not retrieve {favicon_url}: \n{e}")

    # Method 2: site root/favicon.ico
    try:
        parsed = urlparse(url)
        parsed = parsed._replace(path="/favicon.ico")
        favicon_url = parsed.geturl()
        return _request_favicon(favicon_url)
    except Exception as e:
        logger.debug(f"Could not retrieve {favicon_url}.\n{e}")

    raise FaviconURLRetrievalFailed(url=url)


if __name__ == "__main__":
    favicon = get_favicon(sys.argv[1])
    with open("/Users/me/favicon.ico", "wb") as file_:
        file_.write(favicon)
