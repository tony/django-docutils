"""<kbd> (Keyboard Input Element) role for Docutils."""
import typing as t

from docutils import nodes
from docutils.parsers.rst.states import Inliner


def kbd_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> t.Tuple[t.List[nodes.raw], t.List[t.Any]]:
    """Role for ``<kbd>``, the keyboard input element.

    Examples
    --------
    :kbd:`ctrl-t`

    .. code-block:: rst

       :kbd:`ctrl-t`
    """
    html = ""
    keys = text.split(",")

    if isinstance(keys, str):
        keys = [keys]

    for key in keys:
        html += f"<kbd>{key}</kbd>"

    return [nodes.raw("", html, format="html")], []
