"""File role for Docutils."""
import os
import typing as t

from docutils import nodes, utils
from docutils.parsers.rst.states import Inliner


def file_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> t.Tuple[t.List[nodes.emphasis], t.List[t.Any]]:
    """Role for files.

    Examples
    --------
    *📄 ./path/to/moo*:

    .. code-block:: rst

       :file:`./path/to/moo`

    *📁 ./path/to/moo/*:

    .. code-block:: rst

       :file:`./path/to/moo/`
    """
    if options is None:
        options = {}
    name = name.lower()
    title = utils.unescape(text)

    # 'file' would collide with bulma, so we use 'filepath'
    # https://github.com/jgthms/bulma/blob/c2fae71/sass/elements/form.sass#L218
    # https://github.com/jgthms/bulma/issues/1442
    classes = []

    # add .fa class since this isn't a link
    classes.append("far")

    if title.endswith("/"):
        classes.append("fa-folder")
    else:
        classes.append("fa-file-alt")
        extension = os.path.splitext(title)[1]
        if extension:
            classes.append(extension.lstrip("."))

    sn = nodes.emphasis(title, title)

    # insert <span class="fa ..."> inside the <em>
    sn.insert(0, nodes.inline("", "", classes=classes))
    return [sn], []


def manifest_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> t.Tuple[t.List[nodes.emphasis], t.List[t.Any]]:
    """Role for manifests (package.json, file outputs).

    Examples
    --------
    *📄 package.json*:

    .. code-block:: rst

       :manifest:`package.json`

    """
    if options is None:
        options = {}
    name = name.lower()
    title = utils.unescape(text)

    classes = ["manifest"]

    # add .fa class since this isn't a link
    classes.append("fa-file-alt far")

    sn = nodes.emphasis(title, title)

    # insert <span class="fa ..."> inside the <em>
    sn.insert(0, nodes.inline("", "", classes=classes))
    return [sn], []


def exe_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> t.Tuple[t.List[nodes.emphasis], t.List[t.Any]]:
    """Role for executables.

    Examples
    --------
    *📄 ./path/to/webpack*:

    .. code-block:: rst

       :exe:`./path/to/webpack`
    """
    if options is None:
        options = {}
    name = name.lower()
    title = utils.unescape(text)

    classes = ["exe", "fa"]

    sn = nodes.emphasis(title, title)

    # insert <span class="fa ..."> inside the <em>
    sn.insert(0, nodes.inline("", "", classes=classes))
    return [sn], []
