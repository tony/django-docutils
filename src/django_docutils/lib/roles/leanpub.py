"""Leanpub role for Docutils."""
import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import RoleFnReturnValue


def leanpub_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
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
