from django.conf import settings

BASED_LIB_RST = getattr(
    settings,
    'BASED_LIB_RST',
    {
        "font_awesome": {
            "url_patterns": {
                r'.*twitter.com.*': 'fab fa-twitter',
            }
        }
    },
)
