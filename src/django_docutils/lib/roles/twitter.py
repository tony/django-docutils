"""Twitter role for docutils."""
import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import RoleFnReturnValue


def twitter_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
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
