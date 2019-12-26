from docutils import nodes


class pending_xref(nodes.Inline, nodes.Element):

    """Node for cross-references that cannot be resolved without complete
    information about all documents.

    These nodes are resolved before writing output, in
    BuildEnvironment.resolve_references.
    """
