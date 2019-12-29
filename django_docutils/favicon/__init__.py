"""Favicons

Short term:

In the short term, we can use something similar the XRef transform, ran after
that, which downloads and caches favicons.


Long term:

In the future, for this to work at scale, favicons will need to be traversed
ahead of time.

First, there will to be a way to iterate the content of all Node model
object's content. This can be done via::

    for content in PostPage.objects.all().values_list('body'):
        # get the doctree of content
        # traverse content nodes.reference
        # collect all domains/subdomains
        # pull favicons for them and store in Favicon model

"""
