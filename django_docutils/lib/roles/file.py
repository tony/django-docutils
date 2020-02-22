import os

from docutils import nodes, utils


def file_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for files.

    :file:`./path/to/moo` ->
       text: ./path/to/moo (italicized + file icon)

    :file:`./path/to/moo/` ->
       text: ./path/to/moo/ (italicized + directory icon)

    """
    name = name.lower()
    title = utils.unescape(text)

    # 'file' would collide with bulma, so we use 'filepath'
    # https://github.com/jgthms/bulma/blob/c2fae71/sass/elements/form.sass#L218
    # https://github.com/jgthms/bulma/issues/1442
    classes = []

    # add .fa class since this isn't a link
    classes.append('far')

    if title.endswith('/'):
        classes.append('fa-folder')
    else:
        classes.append('fa-file-alt')
        extension = os.path.splitext(title)[1]
        if extension:
            classes.append(extension.lstrip('.'))

    sn = nodes.emphasis(title, title)

    # insert <span class="fa ..."> inside the <em>
    sn.insert(0, nodes.inline('', '', classes=classes))
    return [sn], []


# TODO: Let font-awesome classes be configured via settings
def manifest_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for manifests (package.json, file outputs)

    :manifest:`package.json` ->
       text: package.json (italicized + file icon)

    """
    name = name.lower()
    title = utils.unescape(text)

    classes = ['manifest']

    # add .fa class since this isn't a link
    classes.append('fa-file-alt far')

    sn = nodes.emphasis(title, title)

    # insert <span class="fa ..."> inside the <em>
    sn.insert(0, nodes.inline('', '', classes=classes))
    return [sn], []


def exe_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for executables.

    :exe:`./path/to/webpack` ->
       text: ./path/to/webpack (italicized + file icon)

    """
    name = name.lower()
    title = utils.unescape(text)

    classes = ['exe', 'fa']

    sn = nodes.emphasis(title, title)

    # insert <span class="fa ..."> inside the <em>
    sn.insert(0, nodes.inline('', '', classes=classes))
    return [sn], []
