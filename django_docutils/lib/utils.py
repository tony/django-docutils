"""Docutils util functions and regexes.

Some stuff is ported from sphinx:

- explicit_title_re, ws_re, set_role_source_info, split_explicit_title
"""
import re

from docutils import nodes

if False:
    from typing import Any, Tuple, Type, unicode  # NOQA

    from docutils import nodes  # NOQA
    from sphinx import Pattern

# \x00 means the "<" was backslash-escaped (from sphinx)
explicit_title_re = re.compile(r'^(.+?)\s*(?<!\x00)<(.*?)>$', re.DOTALL)

ws_re = re.compile(r'\s+')  # type: Pattern


def split_explicit_title(text):
    # type: (unicode) -> Tuple[bool, unicode, unicode]
    """Split role content into title and target, if given (from sphinx)."""
    match = explicit_title_re.match(text)  # type: ignore
    if match:
        return True, match.group(1), match.group(2)
    return False, text, text


def chop_after_docinfo(source):
    """Return the source of a document after DocInfo metadata.

    :param source: Source of RST document
    :type source: string
    :returns: All source content after docinfo
    :rtype: string
    """
    # find the last docinfo element
    index = re.findall(r':[\w_]+: [\w \-_\,]+\n', source)[-1]

    # find the character position of last docinfo element + len of it
    rest = source[source.rindex(index) + len(index) :]
    return rest.strip()


def chop_after_title(source):
    """Return the source of a document after DocInfo metadata.

    :param source: Source of RST document
    :type source: string
    :returns: All source content after docinfo
    :rtype: string
    """
    # find the last docinfo element
    index = re.findall(r'[=-]{3,}\n.*\n[-=]{3,}', source, re.MULTILINE)[-1]

    # find the character position of last docinfo element + len of it
    rest = source[source.rindex(index) + len(index) :]
    return rest.strip()


def chop_after_heading_smartly(source):
    """Return the content after subtitle, or, if exists, docinfo.

    This is a universal chop that can be used whether a document has docinfo,
    a title, subtitle, or not. Traditionally, directory-style RST fixtures keep
    metadata inside a JSON file instead of docinfo, so
    :func:`chop_after_docinfo` wouldn't work.

    :param source: Source of RST document
    :type source: string
    :returns: All source content after docinfo or title
    :rtype: string
    """
    try:
        return chop_after_docinfo(source)
    except IndexError:
        return chop_after_title(source)


def find_root_sections(document):
    """Yield top level section nodes

    :param document: docutils document
    :type document: :class:`docutils.nodes.document`
    :yields: upper level titles of document
    :rtype: :class:`docutils.nodes.Node`
    """
    for node in document:
        if isinstance(node, nodes.section):  # traverse root-level sections
            yield node


def append_html_to_node(node, ad_code):
    """Inject HTML in this node

    :param node: node of the section to find last paragraph of
    :type node: :class:`docutils.nodes.node`
    :param ad_code: html to inject inside ad
    :type ad_code: string
    """
    html = '<div class="has-text-centered">'
    html += ad_code
    html += '</div>'

    html_node = nodes.raw('', html, format='html')

    node.append(html_node)
    node.replace_self(node)
