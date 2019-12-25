from docutils import nodes


class icon(nodes.Inline, nodes.TextElement):
    pass


nodes._add_node_class_names('icon')
