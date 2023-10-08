"""PyPI (Python Package Index) role for docutils."""
import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import RoleFnReturnValue


def pypi_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> RoleFnReturnValue:
    """Role for linking to PyPI (Python Package Index) page.

    Returns
    -------
    :data:`django_docutils.lib.roles.types.RoleFnReturnValue`

    Examples
    --------
    `libsass <https://pypi.python.org/pypi/libsass>`_:

    .. code-block:: rst

       :pypi:`libsass`

    `a pypi package <https://pypi.python.org/pypi/libsass>`_:

    .. code-block:: rst

       :pypi:`a pypi package <libsass>`
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        return f"https://pypi.python.org/pypi/{target}"

    return generic_url_role(name, text, url_handler)
