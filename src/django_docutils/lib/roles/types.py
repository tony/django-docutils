import typing as t

from docutils import nodes
from typing_extensions import Protocol


class UrlHandlerFn(Protocol):
    def __call__(self, target: str) -> str:
        ...


class RemoteUrlHandlerFn(Protocol):
    def __call__(self, target: str) -> t.Tuple[str, str]:
        ...


GenericUrlRoleFn = t.Tuple[t.List[nodes.reference], t.List[t.Any]]
