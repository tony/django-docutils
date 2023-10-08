"""Email role for docutils."""
import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import RoleFnReturnValue


def email_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
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

       :email:`me@localhost`
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        return f"mailto:{target}"

    return generic_url_role(name, text, url_handler)
