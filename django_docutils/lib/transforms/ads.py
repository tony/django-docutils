import random

from django.conf import settings
from docutils import nodes
from docutils.transforms import Transform

from django_docutils.lib.utils import append_html_to_node, find_root_sections

"""
Ideas:

Create a generic Ad class that can counter the number of times it's
posted, and render itself. It can be used to wrap Google and Amazon ads.

If content is < 1000 TOTAL across all sections, show NO ads whatsoever

"""


class InjectAds(Transform):

    """Add AdSense Javascript after the second nodes.section in Writer.

    Finding the node:

    1. First preference, use the second node (usually it picks this)
    2. But if the node's text ends with a :, continue to traverse nodes
    """

    default_priority = 100

    #: list of keywords for the ad system, default 'linux'
    ad_keywords = ['linux']

    #: minimum amount of chars in a section to show and add
    #: https://support.google.com/adsense/answer/1346295?hl=en#Ad_limit_per_page  # NOQA
    ad_section_length_min = 1000

    #: minimum content on page to show an ad
    #: showing ads where there isn't enough content sucks
    ad_page_length_min = ad_section_length_min

    #: max ads per page
    ads_max = 3

    @classmethod
    def keywords(cls, ad_keywords):
        if ad_keywords:
            cls.ad_keywords = ad_keywords
        return cls

    def apply(self):
        section_nodes = list(find_root_sections(self.document))

        ads_posted = 0

        page_length = 0

        for node in section_nodes:
            # Don't show Google ads on sections that are too small
            section_length = 0
            for p in node.traverse(nodes.paragraph):
                section_length += len(p.astext())

            # add this section size to the current page length
            page_length += section_length

            if section_length < self.ad_section_length_min:
                continue

            ad_code = random.choice(
                [
                    settings.BASED_ADS['GOOGLE_AD_CODE'],
                    settings.BASED_ADS['AMAZON_AD_STRIP'],
                ]
            )
            # ad_code = settings.BASED_ADS['AMZN_AD_CODE'].format(
            #     keyword=self.ad_keywords[0]
            # )

            # append node to end of section
            append_html_to_node(node, ad_code)
            ads_posted += 1

            if ads_posted >= self.ads_max:
                break

        # if no ads posted, inject in last section
        if not ads_posted and page_length > self.ad_page_length_min:
            try:
                last_section = section_nodes[-1]
            except IndexError:  # there's no sections after main title
                last_section = self.document

            node = last_section[-1]  # end of section

            append_html_to_node(node, settings.BASED_ADS['GOOGLE_AD_CODE'])
