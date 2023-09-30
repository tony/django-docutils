import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import GenericUrlRoleFn


def email_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> GenericUrlRoleFn:
    """Role for linking to email articles.

    :email:`me@localhost` ->
       link: mailto:me@localhost
       text: me@localhost

    :email:`E-mail me <me@localhost>` ->
       link: mailto:me@localhost
       text: E-mail me
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        return f"mailto:{target}"

    return generic_url_role(name, text, url_handler)
