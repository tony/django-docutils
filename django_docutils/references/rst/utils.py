from typing import Any

from docutils import nodes


def set_role_source_info(inliner: Any, lineno: int, node: nodes.Node):
    """From sphinx, for intersphinx"""
    node.source, node.line = inliner.reporter.get_source_and_line(lineno)
