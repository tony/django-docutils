"""Email role for docutils."""

from __future__ import annotations

import typing as t

from .common import generic_url_role

if t.TYPE_CHECKING:
    from docutils.parsers.rst.states import Inliner

    from .types import RoleFnReturnValue


def email_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: dict[str, t.Any] | None = None,
    content: str | None = None,
) -> RoleFnReturnValue:
    """Role for linking to email articles.

    Returns
    -------
    :data:`django_docutils.lib.roles.types.RoleFnReturnValue`

    Examples
    --------
    `me@localhost <mailto:me@localhost>`_:

    .. code-block:: rst

       :email:`me@localhost`

    `Email me <mailto:me@localhost>`_:

    .. code-block:: rst

       :email:`Email me <me@localhost>`
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        return f"mailto:{target}"

    return generic_url_role(name, text, url_handler)
