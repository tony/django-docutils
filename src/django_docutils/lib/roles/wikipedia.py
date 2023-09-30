import typing as t
from urllib.parse import quote

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import GenericUrlRoleFn


def wikipedia_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> GenericUrlRoleFn:
    """Role for linking to Wikipedia articles.

    :wikipedia:`Don't repeat yourself` ->
       link: https://en.wikipedia.org/wiki/Don%27t_repeat_yourself
       text: Don't repeat yourself


    :wikipedia:`this wikipedia article <vim-airline>` ->
       link: https://github.com/vim-airline
       text: this wikipedia article
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        target = quote(target.replace(" ", "_"))
        return f"https://en.wikipedia.org/wiki/{target}"

    return generic_url_role(name, text, url_handler)
