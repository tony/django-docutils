import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import GenericUrlRoleFn


def github_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> GenericUrlRoleFn:
    """Role for linking to GitHub repos and issues.

    :gh:`vim-airline` ->
       link: https://github.com/vim-airline
       text: vim-airline


    :gh:`vim-airline's org <vim-airline>` ->
       link: https://github.com/vim-airline
       text: vim-airline's org

    :gh:`vim-airline/vim-airline` ->
       link: https://github.com/vim-airline/vim-airline
       text: vim-airline/vim-airline

    :gh:`vim-airline/vim-airline#134` ->
       link: https://github.com/vim-airline/vim-airline/issues/134
       text: vim-airline/vim-airline#134

    :gh:`this example issue <vim-airline/vim-airline#134>` ->
       link: https://github.com/vim-airline/vim-airline/issues/134
       text: this example issue
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        if "#" in target:
            user_n_repo, issue = target.split("#")
            if issue.isnumeric():
                return f"https://github.com/{user_n_repo}/issues/{issue}"

        return f"https://github.com/{target}"

    return generic_url_role(name, text, url_handler)
