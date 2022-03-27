import logging

import tldextract
from django.core.files.uploadedfile import SimpleUploadedFile
from tqdm import tqdm, trange

from django_docutils.favicon.models import get_favicon_model
from django_docutils.favicon.rst.transforms.favicon import plain_references
from django_docutils.favicon.scrape import get_favicon

logger = logging.getLogger(__name__)
Favicon = get_favicon_model()


def yield_references(document, url_pattern=None):
    """Yield site pages in a docutils document format

    :param document:
    :type document: :class:`docutils.nodes.document`
    :rtype: string
    :yields: Document of pages in side
    """
    nodes = document.traverse(plain_references)
    for node in nodes:
        if url_pattern:  # if --pattern entered
            if url_pattern not in node["refuri"]:
                continue

        yield node["refuri"]


def prefetch_favicons(url_pattern=None, PostPage=None):
    # PostPage=get_postpage_models()[0]
    urls = []
    t = trange(PostPage.objects.count())

    # iterate through all page documents on the sites
    for page_document in yield_page_doctrees(PostPage):
        # iterate through all references inside the document
        urls.extend(yield_references(page_document, url_pattern))
        t.update(1)

    t = tqdm(urls)
    for url in t:
        prefetch_favicon(url, progress=t)


def is_favicon_stored(fqdn):
    """Assure the favicon *and its file* exist in storage

    This is split up for testing critical logic. There is a race condition
    where the object exists in the database, but the file in not in storage.

    prefetch_favicon must be resilient enough to download the image if its
    not existing in storage.
    """
    # don't redown if fqdn favicon already exists
    try:
        favicon = Favicon.objects.get(domain=fqdn)

        # check for the file itself
        try:
            if favicon.favicon.file:
                logger.debug(
                    "{} for {} already exists, skipping".format(
                        favicon.favicon.file, fqdn
                    )
                )
                return True  # Favicon for fqdn + file already exists
        except FileNotFoundError:
            pass  # that's fine, we'll download it again!
    except Favicon.DoesNotExist:
        pass  # that's fine! we'll add it

    return False


def prefetch_favicon(url, progress=None):
    """Download a store a favicon for a site, if it exists.

    Intended for use when running in situ transforms on :class:`
    docutils.nodes.reference` traversals of URL's. This will look up the
    fqdn (fully qualified domain name) for a URL, check against the Favicon
    models for any results, if they don't exist, it'll try to scrape the
    favicon from the fqdn, store it, and store the path in a Favicon entry for
    that fqdn.

    :param url: URL to any page on a website
    :type url: str
    :rtype: (model, created date)|None
    """
    fqdn = tldextract.extract(url).fqdn

    # optional tqdm progress bar pass-in
    if progress:
        progress.set_description(f"Downloading favicon {fqdn}")

    if is_favicon_stored(fqdn):  # don't redownload
        return

    try:
        favicon_content = get_favicon(url)
    except Exception as e:
        logger.debug(f"Error occurred fetch icon for {fqdn}: {e}")
        return

    return Favicon.objects.update_or_create(
        domain=fqdn,
        defaults={
            "domain": fqdn,
            "favicon": SimpleUploadedFile(
                name=f"{fqdn}.ico",
                content=favicon_content,
                content_type="image/ico",
            ),
        },
    )


def yield_page_doctrees(PostPage):
    """Yield site pages in a docutils document format

    :param PostPage: Any model implementing PostPageBase
    :type: :class:`django_docutils.rst_post.models.RSTPostPageBase`
    :yields: Document of pages in side
    :rtype: :class:`docutils.nodes.document`
    """
    for page in PostPage.objects.all():
        yield page.document
