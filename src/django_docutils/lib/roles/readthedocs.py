import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import GenericUrlRoleFn


def readthedocs_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> GenericUrlRoleFn:
    """Role for linking to readthedocs.org page.

    :rtd:`django-pipeline` ->
       link: https://django-pipeline.readthedocs.io/
       text: django-pipeline

    :rtd:`a rtd site <django-pipeline>` ->
       link: https://django-pipeline.readthedocs.io/
       text: a rtd site

    :rtd:`python-guide:dev/virtualenvs` ->
       link: https://python-guide.readthedocs.io/en/latest/dev/virtualenvs/
       text: python-guide:dev/virtualenvs

    :rtd:`about virtualenvs <python-guide:dev/virtualenvs>` ->
       link: https://python-guide.readthedocs.io/en/latest/dev/virtualenvs/
       text: about virtalenvs
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        if ":" in target:
            project, path = target.split(":")
            return f"https://{project}.readthedocs.io/en/latest/{path}"
        return f"https://{target}.readthedocs.io"

    return generic_url_role(name, text, url_handler)
