"""Leanpub role for Docutils."""

from __future__ import annotations

import typing as t

from .common import generic_url_role

if t.TYPE_CHECKING:
    from docutils.parsers.rst.states import Inliner

    from .types import RoleFnReturnValue


def leanpub_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: dict[str, t.Any] | None = None,
    content: str | None = None,
) -> RoleFnReturnValue:
    """Role for linking to leanpub page.

    Returns
    -------
    :data:`django_docutils.lib.roles.types.RoleFnReturnValue`

    Examples
    --------
    `the-tao-of-tmux <https://leanpub.com/the-tao-of-tmux>`_:

    .. code-block:: rst

       :leanpub:`the-tao-of-tmux`

    `my book <https://leanpub.com/the-tao-of-tmux>`_:

    .. code-block:: rst

       :leanpub:`my book <the-tao-of-tmux>`

    `The Tao of tmux <https://leanpub.com/the-tao-of-tmux/read>`_:

    .. code-block:: rst

       :leanpub:`The Tao of tmux <the-tao-of-tmux:read>`
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        if ":" in target:
            project, path = target.split(":")
            return f"https://leanpub.com/{project}/{path}"
        return f"https://leanpub.com/{target}"

    return generic_url_role(name, text, url_handler)
