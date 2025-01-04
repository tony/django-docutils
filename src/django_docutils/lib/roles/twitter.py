"""Twitter role for docutils."""

from __future__ import annotations

import typing as t

from .common import generic_url_role

if t.TYPE_CHECKING:
    from docutils.parsers.rst.states import Inliner

    from .types import RoleFnReturnValue


def twitter_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: dict[str, t.Any] | None = None,
    content: str | None = None,
) -> RoleFnReturnValue:
    """Role for linking to twitter articles.

    Returns
    -------
    :data:`django_docutils.lib.roles.types.RoleFnReturnValue`

    Examples
    --------
    `@username <https://twitter.com/username>`_:

    .. code-block:: rst

       :twitter:`@username`

    `follow me on twitter <https://twitter.com/username>`_:

    .. code-block:: rst

       :twitter:`follow me on twitter <@username>`
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        if "@" in target:
            target = target.replace("@", "")

        return f"https://twitter.com/{target}"

    return generic_url_role(name, text, url_handler)
