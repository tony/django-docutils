"""HN (HackerNews) role for Docutils."""
import typing as t
from urllib.parse import quote

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import RoleFnReturnValue


def hackernews_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> RoleFnReturnValue:
    """Role for linking to hackernews articles.

    Returns
    -------
    :data:`django_docutils.lib.roles.types.RoleFnReturnValue`

    Examples
    --------
    `15610489 <https://news.ycombinator.com/item?id=15610489>`_:

    .. code-block:: rst

      :hn:`15610489`

    `this hackernews article <https://news.ycombinator.com/item?id=15610489>`_:

    .. code-block:: rst

       :hn:`this hackernews article <15610489>`
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        target = quote(target.replace(" ", "_"))
        return f"https://news.ycombinator.com/item?id={target}"

    return generic_url_role(name, text, url_handler)
