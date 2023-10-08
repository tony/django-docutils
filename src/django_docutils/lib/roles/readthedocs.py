"""ReadTheDocs role for Docutils."""
import typing as t

from docutils.parsers.rst.states import Inliner

from .common import generic_url_role
from .types import RoleFnReturnValue


def readthedocs_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: t.Optional[t.Dict[str, t.Any]] = None,
    content: t.Optional[str] = None,
) -> RoleFnReturnValue:
    """Role for linking to readthedocs.org page.

    Returns
    -------
    :data:`django_docutils.lib.roles.types.RoleFnReturnValue`

    Examples
    --------
    `django-pipeline <https://django-pipeline.readthedocs.io/>`_:

    .. code-block:: rst

       :rtd:`django-pipeline`

    `a rtd site <https://django-pipeline.readthedocs.io/>`_:

    .. code-block:: rst

       :rtd:`a rtd site <django-pipeline>`

    `python-guide:dev/virtualenvs <https://python-guide.readthedocs.io/en/latest/dev/virtualenvs/>`_:

    .. code-block:: rst

       :rtd:`python-guide:dev/virtualenvs`

    `about virtualenvs <https://python-guide.readthedocs.io/en/latest/dev/virtualenvs/>`_:

    .. code-block:: rst

       :rtd:`about virtualenvs <python-guide:dev/virtualenvs>`
    """
    if options is None:
        options = {}

    def url_handler(target: str) -> str:
        if ":" in target:
            project, path = target.split(":")
            return f"https://{project}.readthedocs.io/en/latest/{path}"
        return f"https://{target}.readthedocs.io"

    return generic_url_role(name, text, url_handler)
