import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import GenericUrlRoleFn


def twitter_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> GenericUrlRoleFn:
    """Role for linking to twitter articles.

    Returns
    -------
    :data:`django_docutils.lib.roles.types.GenericUrlRoleFn`

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
