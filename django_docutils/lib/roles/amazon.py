from urllib.error import HTTPError

from bitly_api import bitly_api
from django.conf import settings

from django_docutils.references.models import get_reference_model

from .common import generic_remote_url_role

Reference = get_reference_model()


def get_client():
    from amazon.api import AmazonAPI

    return AmazonAPI(
        settings.AMAZON_PRODUCT_API_ACCESS_KEY,
        settings.AMAZON_PRODUCT_API_SECRET_KEY,
        settings.AMAZON_ASSOCIATES_TRACKING_ID,
    )


def amazon_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for linking to amazon product.

    First, try to resolve via memoization (redis kv store).
    Second, try to resolve via database back-end.
    Finally, try to resolve via remote API call, which saves to
        the database of references.

    In the future, create a wrapper / function / decorator to automate this
    for remote API roles.

    :amzn:`B01MG342KU` ->
       link: amazn shortline
       text: The Tao of tmux: and Terminal Tricks

    :amzn:`my book <B01MG342KU>` ->
       link: amzn shortlink
       text: my book
    """
    amzn = get_client()

    def url_handler(target):
        try:
            r = Reference.objects.get(project='amazon', target=target)
        except Reference.DoesNotExist:
            query = amzn.lookup(ItemId=target)
            url = query.offer_url

            access_token = settings.BITLY_ACCESS_TOKEN
            bitly = bitly_api.Connection(access_token=access_token)
            url = bitly.shorten(url)['url']

            r = Reference(
                project='amazon',
                type=name,
                target=target,
                display_name=query.title,
                uri=url,
            )
            r.save()
        return r.display_name, r.uri

    try:
        return generic_remote_url_role(name, text, url_handler)
    except HTTPError:
        msg = inliner.reporter.error(
            'Error connecting to amazon API for "%s"' % text, line=lineno
        )
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
