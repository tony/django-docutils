"""PyPI (Python Package Index) role for docutils."""

from __future__ import annotations

import typing as t

from .common import generic_url_role

if t.TYPE_CHECKING:
    from docutils.parsers.rst.states import Inliner

    from .types import RoleFnReturnValue


def pypi_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: dict[str, t.Any] | None = None,
    content: str | None = None,
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
