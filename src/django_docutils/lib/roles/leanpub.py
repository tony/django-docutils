import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import GenericUrlRoleFn


def leanpub_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> GenericUrlRoleFn:
    """Role for linking to leanpub page.

    :leanpub:`the-tao-of-tmux` ->
       link: https://leanpub.com/the-tao-of-tmux
       text: the-tao-of-tmux

    :leanpub:`my book <the-tao-of-tmux>` ->
       link: https://leanpub.com/the-tao-of-tmux
       text: my book

    :leanpub:`The Tao of tmux <the-tao-of-tmux:read>` ->
       link: https://leanpub.com/the-tao-of-tmux/read
       text: The Tao of tmux
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        if ":" in target:
            project, path = target.split(":")
            return f"https://leanpub.com/{project}/{path}"
        return f"https://leanpub.com/{target}"

    return generic_url_role(name, text, url_handler)
