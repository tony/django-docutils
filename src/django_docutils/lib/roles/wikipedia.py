"""Wikipedia role for Docutils."""
import typing as t
from urllib.parse import quote

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import RoleFnReturnValue


def wikipedia_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> RoleFnReturnValue:
    """Role for linking to Wikipedia articles.

    Returns
    -------
    :data:`django_docutils.lib.roles.types.RoleFnReturnValue`

    Examples
    --------
    `Don't repeat yourself <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_:

    .. code-block:: rst

       :wikipedia:`Don't repeat yourself`

    `this wikipedia article <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_:

    .. code-block:: rst

       :wikipedia:`this wikipedia article <Don't repeat yourself>`
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        target = quote(target.replace(" ", "_"))
        return f"https://en.wikipedia.org/wiki/{target}"

    return generic_url_role(name, text, url_handler)
