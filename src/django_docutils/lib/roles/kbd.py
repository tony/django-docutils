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
    html = ""
    keys = text.split(",")

    if isinstance(keys, str):
        keys = [keys]

    for key in keys:
        html += f"<kbd>{key}</kbd>"

    return [nodes.raw("", html, format="html")], []
