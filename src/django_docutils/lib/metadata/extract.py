"""Title, Subtitle, and Metadata extraction of reStructuredText."""
import typing as t

from django.template.defaultfilters import truncatewords
from django.utils.html import strip_tags
from docutils import nodes


def extract_title(document: nodes.document) -> t.Optional[str]:
    """Return the title of the document.

    Parameters
    ----------
    document : :class:`docutils.nodes.document`
        Document to return title for.

    Returns
    -------
    str or None
        Title of document or None if not found.
    """
    for node in document.traverse(nodes.PreBibliographic):  # type:ignore
        if isinstance(node, nodes.title):
            return node.astext()
    return None


def extract_metadata(document: nodes.document) -> t.Dict[str, str]:
    """Return the dict containing document metadata.

    Parameters
    ----------
    document : :class:`docutils.nodes.document`
        Document extract metadata from.

    Returns
    -------
    dict
        docinfo data from document

    See Also
    --------
    From: https://github.com/adieu/mezzanine-cli @ mezzanine_cli/parser.py
    License: BSD (https://github.com/adieu/mezzanine-cli/blob/master/setup.py)
    """
    output = {}
    for docinfo in document.traverse(nodes.docinfo):
        for element in docinfo.children:
            if not isinstance(element, nodes.Text) and not isinstance(
                element,
                nodes.Element,
            ):
                continue

            if element.tagname == "field":  # custom fields (e.g. summary)
                name_elem, body_elem = element.children
                assert isinstance(name_elem, (nodes.Text, nodes.Element))
                assert isinstance(body_elem, (nodes.Text, nodes.Element))
                name = name_elem.astext()
                value = body_elem.astext()
            elif isinstance(
                element,
                (nodes.Text, nodes.TextElement),
            ):  # standard fields (e.g. address)
                name = element.tagname
                value = element.astext()
            else:
                msg = f"No support for {element} of type {type(element)}"
                raise NotImplementedError(
                    msg,
                )
            name = name.lower()

            output[name] = value
    return output


def extract_subtitle(document: nodes.document) -> t.Optional[str]:
    """Return the subtitle of the document."""
    for node in document.traverse(nodes.PreBibliographic):  # type:ignore
        if isinstance(node, nodes.subtitle):
            return node.astext()
    return None


def extract_abstract(doctree: nodes.document, length: int = 100) -> str:
    """Pull first n words from a docutils document.

    We use this to create snippets for Twitter Cards, FB, etc.

    Parameters
    ----------
    doctree : :class:`docutils.nodes.document`
        Document to extract abstract from.
    length : int
        Word count to cut content off at.

    Returns
    -------
    str
        truncated content, html tags removed
    """
    paragraph_nodes = doctree.traverse(nodes.paragraph)
    text = ""
    for node in paragraph_nodes:
        text += node.astext()
        if len(text.split(" ")) > 100:
            break
    return truncatewords(strip_tags(text), 100)
