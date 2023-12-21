"""Docutils util functions and regexes.

Some stuff is ported from sphinx:

- explicit_title_re, ws_re, set_role_source_info, split_explicit_title
"""
import re
import typing as t

from docutils import nodes

# \x00 means the "<" was backslash-escaped (from sphinx)
explicit_title_re = re.compile(r"^(.+?)\s*(?<!\x00)<(.*?)>$", re.DOTALL)

ws_re: "re.Pattern[str]" = re.compile(r"\s+")


def split_explicit_title(text: str) -> t.Tuple[bool, str, str]:
    """Split role content into title and target, if given (from sphinx)."""
    match = explicit_title_re.match(text)
    if match:
        return True, match.group(1), match.group(2)
    return False, text, text


def chop_after_docinfo(source: str) -> str:
    """Return the source of a document after DocInfo metadata.

    Parameters
    ----------
    source : str
        Source of RST document

    Returns
    -------
    str
        All source content after docinfo
    """
    # find the last docinfo element
    index = re.findall(r":[\w_]+: [\w \-_\,]+\n", source)[-1]

    # find the character position of last docinfo element + len of it
    rest = source[source.rindex(index) + len(index) :]
    return rest.strip()


def chop_after_title(source: str) -> str:
    """Return the source of a document after document title.

    Parameters
    ----------
    source : str
        Source of RST document

    Returns
    -------
    str
        All source content after title
    """
    # find the last docinfo element
    index = re.findall(r"[=-]{3,}\n.*\n[-=]{3,}", source, re.MULTILINE)[-1]

    # find the character position of last docinfo element + len of it
    rest = source[source.rindex(index) + len(index) :]
    return rest.strip()


def chop_after_heading_smartly(source: str) -> str:
    """Return the content after subtitle, or, if exists, docinfo.

    This is a universal chop that can be used whether a document has docinfo,
    a title, subtitle, or not. Traditionally, directory-style RST fixtures keep
    metadata inside a JSON file instead of docinfo, so
    :func:`chop_after_docinfo` wouldn't work.

    Parameters
    ----------
    source : str
        Source of RST document

    Returns
    -------
    str
        All source content after docinfo or title
    """
    try:
        return chop_after_docinfo(source)
    except IndexError:
        return chop_after_title(source)


def find_root_sections(document: nodes.document) -> t.Generator[nodes.Node, None, None]:
    """Yield top level section nodes.

    Parameters
    ----------
    document : :class:`docutils.nodes.document`
        Docutils document

    Yields
    ------
    :class:`docutils.nodes.Node`
        Upper level titles of document
    """
    for node in document.findall(nodes.section):
        yield from node


def append_html_to_node(node: nodes.Element, ad_code: str) -> None:
    """Inject HTML in this node.

    Parameters
    ----------
    node : :class:`docutils.nodes.node`
        node of the section to find last paragraph of
    ad_code : str
        html to inject inside ad
    """
    html = '<div class="has-text-centered">'
    html += ad_code
    html += "</div>"

    html_node = nodes.raw("", html, format="html")

    node.append(html_node)
    node.replace_self(node)

    return None
