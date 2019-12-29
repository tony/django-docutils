from urllib.parse import quote

from .common import generic_url_role


def hackernews_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for linking to hackernews articles.

    :hn:`15610489` ->
       link: https://news.ycombinator.com/item?id=15610489
       text: 15610489


    :hn:`this hackernews article <15610489>` ->
       link: https://news.ycombinator.com/item?id=15610489
       text: this hackernews article
    """

    def url_handler(target):
        target = quote(target.replace(' ', '_'))
        return f'https://news.ycombinator.com/item?id={target}'

    return generic_url_role(name, text, url_handler)
