import typing as t
from urllib.parse import quote

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import GenericUrlRoleFn


def hackernews_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> GenericUrlRoleFn:
    """Role for linking to hackernews articles.

    :hn:`15610489` ->
       link: https://news.ycombinator.com/item?id=15610489
       text: 15610489


    :hn:`this hackernews article <15610489>` ->
       link: https://news.ycombinator.com/item?id=15610489
       text: this hackernews article
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        target = quote(target.replace(" ", "_"))
        return f"https://news.ycombinator.com/item?id={target}"

    return generic_url_role(name, text, url_handler)
