from docutils import nodes


def kbd_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    html = ''
    keys = text.split(',')

    if isinstance(keys, str):
        keys = [keys]

    for key in keys:
        html += f'<kbd>{key}</kbd>'

    return [nodes.raw('', html, format='html')], []
