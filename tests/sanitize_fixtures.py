"""Test fixtures for sanitizer ordering.

Importable by dotted path because ``pythonpath`` includes ``tests`` (see
``pyproject.toml``), so ``DJANGO_DOCUTILS_LIB_RST['transforms']`` can reference
``sanitize_fixtures.InjectingTransform``.
"""

from __future__ import annotations

import typing as t

from docutils import nodes
from docutils.transforms import Transform


class InjectingTransform(Transform):
    """Writer transform that injects unsafe nodes a user could not write.

    Stands in for a third-party transform that builds nodes from untrusted
    content without validating schemes or escaping HTML. Its output must be
    stripped by the locked-down sanitizer just like unsafe source markup.
    """

    default_priority = 500

    def apply(self, **kwargs: t.Any) -> None:
        """Append a javascript: link and a raw script node to the document."""
        reference = nodes.reference("", "click", refuri="javascript:alert(1)")
        self.document += nodes.paragraph("", "", reference)
        self.document += nodes.raw("", "<script>alert(2)</script>", format="html")
