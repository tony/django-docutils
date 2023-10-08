"""URL Role for docutils."""
import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import RoleFnReturnValue


def url_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> RoleFnReturnValue:
    """Role for linking to url articles.

    Returns
    -------
    :data:`django_docutils.lib.roles.types.RoleFnReturnValue`

    Examples
    --------
    https://google.com:

    .. code-block:: rst

      :url:`https://google.com`


    `Google <https://google.com>`_:

    .. code-block:: rst

      :url:`Google <https://google.com>`

    |google|_:

    .. |google| replace:: *Google*

    .. _google: https://google.com

    .. code-block:: rst

       :url:`*Google* <https://google.com>`
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        return target

    return generic_url_role(name, text, url_handler)
