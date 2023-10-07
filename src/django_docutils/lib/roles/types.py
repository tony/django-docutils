import typing as t

from docutils import nodes
from typing_extensions import Protocol


class UrlHandlerFn(Protocol):
    """Role function that directly maps to a URL."""

    def __call__(self, target: str) -> str:
        ...


class RemoteUrlHandlerFn(Protocol):
    """Role function that can query an external source for its title."""

    def __call__(self, target: str) -> t.Tuple[str, str]:
        ...


RoleFnReturnValue = t.Tuple[t.List[nodes.reference], t.List[t.Any]]
"""Role function return value.

See also
--------

From `Docutils: How to: RST Roles
<https://docutils.sourceforge.io/docs/howto/rst-roles.html>`_:

    Role functions return a tuple of two values:
    
    - A list of nodes which will be inserted into the document tree at the point where
      the interpreted role was encountered (can be an empty list).
    - A list of system messages, which will be inserted into the document tree
      immediately after the end of the current block (can also be empty).
"""
