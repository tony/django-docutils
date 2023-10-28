"""GitHub role for Docutils."""
import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import RoleFnReturnValue


def github_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> RoleFnReturnValue:
    """Role for linking to GitHub repos and issues.

    Returns
    -------
    RoleFnReturnValue

    Examples
    --------
    `vim-airline <https://github.com/vim-airline>`_:

    .. code-block:: rst

       :gh:`vim-airline`

    `vim-airline's org <https://github.com/vim-airline>`_:

    .. code-block:: rst

       :gh:`vim-airline's org <vim-airline>`

    `vim-airline/vim-airline <https://github.com/vim-airline/vim-airline>`_:

    .. code-block:: rst

       :gh:`vim-airline/vim-airline`

    `vim-airline/vim-airline#125 <https://github.com/vim-airline/vim-airline/issue/125>`_:

    .. code-block:: rst

      :gh:`vim-airline/vim-airline#125`

    `this example issue <https://github.com/vim-airline/vim-airline/issue/125>`_:

    .. code-block:: rst

      :gh:`this example issue <vim-airline/vim-airline#125>`
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        if "#" in target:
            user_n_repo, issue = target.split("#")
            if issue.isnumeric():
                return f"https://github.com/{user_n_repo}/issue/{issue}"

        return f"https://github.com/{target}"

    return generic_url_role(name, text, url_handler)
