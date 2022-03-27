from django.template.defaultfilters import truncatewords
from django.utils.html import strip_tags
from docutils import nodes


def extract_title(document):
    """Return the title of the document.

    :param document:
    :type document: :class:`docutils.nodes.document`
    """
    for node in document.traverse(nodes.PreBibliographic):
        if isinstance(node, nodes.title):
            return node.astext()


def extract_metadata(document):
    """Return the dict containing document metadata.

    :param document:
    :type document: :class:`docutils.nodes.document`
    :returns: docinfo data from document
    :rtype: dict

    From: https://github.com/adieu/mezzanine-cli @ mezzanine_cli/parser.py
    License: BSD (https://github.com/adieu/mezzanine-cli/blob/master/setup.py)
    """
    output = {}
    for docinfo in document.traverse(nodes.docinfo):
        for element in docinfo.children:
            if element.tagname == "field":  # custom fields (e.g. summary)
                name_elem, body_elem = element.children
                name = name_elem.astext()
                value = body_elem.astext()
            else:  # standard fields (e.g. address)
                name = element.tagname
                value = element.astext()
            name = name.lower()

            output[name] = value
    return output


def extract_subtitle(document):
    """Return the subtitle of the document."""
    for node in document.traverse(nodes.PreBibliographic):
        if isinstance(node, nodes.subtitle):
            return node.astext()


def extract_abstract(doctree, length=100):
    """Pull first n words from a docutils document.

    We use this to create snippets for Twitter Cards, FB, etc.

    :param doctree: docutils document to extract from
    :type doctree: :class:`docutils.nodes.document`
    :param length: word count to cut content off at
    :type length: int
    :rtype: string
    :returns: truncated content, html tags removed

    """
    paragraph_nodes = doctree.traverse(nodes.paragraph)
    text = ""
    for node in paragraph_nodes:
        text += node.astext()
        if len(text.split(" ")) > 100:
            break
    return truncatewords(strip_tags(text), 100)
