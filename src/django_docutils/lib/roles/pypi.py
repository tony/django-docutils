import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import GenericUrlRoleFn


def pypi_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> GenericUrlRoleFn:
    """Role for linking to pypi page.

    :pypi:`libsass` ->
       link: https://pypi.python.org/pypi/libsass
       text: libsass


    :pypi:`a pypi package <libsass>` ->
       link: https://pypi.python.org/pypi/libsass
       text: a pypi package
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        return f"https://pypi.python.org/pypi/{target}"

    return generic_url_role(name, text, url_handler)
