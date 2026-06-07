"""<kbd> (Keyboard Input Element) role for Docutils."""

from __future__ import annotations

import typing as t

from docutils import nodes
from docutils.parsers.rst.states import Inliner


def kbd_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: dict[str, t.Any] | None = None,
    content: str | None = None,
) -> tuple[list[nodes.inline], list[t.Any]]:
    """Role for ``<kbd>``, the keyboard input element.

    Examples
    --------
    >>> node_list, messages = kbd_role(
    ...     "kbd",
    ...     ":kbd:`ctrl-t`",
    ...     "ctrl-t",
    ...     1,
    ...     None,  # type: ignore[arg-type]
    ... )
    >>> messages
    []
    >>> node_list[0].astext()
    'ctrl-t'
    >>> node_list[0]["classes"]
    ['kbd']

    .. code-block:: rst

       :kbd:`ctrl-t`
    """
    return [nodes.inline(rawtext, key, classes=["kbd"]) for key in text.split(",")], []
