import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import GenericUrlRoleFn


def url_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> GenericUrlRoleFn:
    """Role for linking to url articles.

    :url:`https://google.com` ->
       link: https://google.com
       text: https://google.com

    :url:`Google <https://google.com>` ->
        link: https://google.com
        text: Google

    :url:`*Google* <https://google.com>` ->
        link: https://google.com
        text (html): <em>Google</em>
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        return target

    return generic_url_role(name, text, url_handler)
