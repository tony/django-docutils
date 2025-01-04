"""HN (HackerNews) role for Docutils."""

from __future__ import annotations

import typing as t
from urllib.parse import quote

from .common import generic_url_role

if t.TYPE_CHECKING:
    from docutils.parsers.rst.states import Inliner

    from .types import RoleFnReturnValue


def hackernews_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: dict[str, t.Any] | None = None,
    content: str | None = None,
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
