"""Docutils writers for Django Docutils, designed for cleaner output."""
import typing as t

from django.conf import settings
from django.utils.module_loading import import_string
from docutils import nodes
from docutils.transforms import Transform
from docutils.writers.html5_polyglot import HTMLTranslator, Writer

from .settings import DJANGO_DOCUTILS_LIB_RST


class ParentNodeClassTuple(t.NamedTuple):
    """Typing for parent node accepting custom arguments."""

    parent_node_type: t.Type[t.Union[nodes.Node, nodes.Body]]
    args: list[str]
    kwargs: t.Dict[str, str]
    close_tag: t.Optional[str]


class DjangoDocutilsHTMLTranslator(HTMLTranslator):
    """Django Docutils touchups to docutil's HTML renderer."""

    def __init__(self, document: nodes.document) -> None:
        HTMLTranslator.__init__(self, document)

    def visit_table(self, node: nodes.Element) -> None:
        """Open table."""
        node["classes"].extend(["table"])
        HTMLTranslator.visit_table(self, node)

    def visit_reference(self, node: nodes.Element) -> None:
        """Open reference.

        Changes:

        - Monkeypatch bugfix https://sourceforge.net/p/docutils/bugs/322/
        - Add target _blank to offsite urls
        - Add class offsite for offsite urls
        - Add class insite for insite urls (note, internal is already used
          for reference links in the *same* document)
        """
        atts = {"class": "reference"}

        if "refuri" in node:
            atts["href"] = node["refuri"]
            if self.settings.cloak_email_addresses and atts["href"].startswith(
                "mailto:",
            ):
                atts["href"] = self.cloak_mailto(atts["href"])
                self.in_mailto = True
            atts["class"] += " external"
            if (
                not any(node["refuri"] in host for host in settings.ALLOWED_HOSTS)
                and not node["refuri"].startswith("#")
                and not node["refuri"].startswith("/")
            ):
                atts["target"] = "_blank"
                atts["class"] += " offsite"
                # sphinx sites, a ref wrapping a nodes.literal is a code link
                if isinstance(node[0], nodes.literal):
                    atts["class"] += " code"
            else:
                atts["class"] += " insite"
        else:
            assert (
                "refid" in node
            ), 'References must have "refuri" or "refid" attribute.'
            atts["href"] = "#" + node["refid"]
            atts["class"] += " internal"

        try:
            from django_docutils.favicon.rst.nodes import icon

            if isinstance(node[0], icon):
                atts["class"] = ""
        except ImportError:
            pass
        self.body.append(self.starttag(node, "a", "", **atts))

    def visit_title(self, node: nodes.Element) -> None:
        """Visit docutils title.

        Changes:

        - Add backlinks for Contents refid headers

          They're baked inside the Section (parent) of the anchor
          since we're using an ad-hoc contents transformation process
          that builds toc separately from the main content (see templatetags)

        - s/with-subtitle/subtitle for bulma css

        """
        close_tag: t.Optional[str] = "</p>\n"

        # add backlinks to refid (toc header backlinks)
        # This assures headers link to themselves, so users can copy a link
        # to the anchor, rather than docutils default behavior of linking back
        # to the doc
        if isinstance(node.parent, nodes.section):
            node["refid"] = node.parent["ids"][0]

        # specific cases we don't use h{1-6} tags for
        parent_node_classes: list[ParentNodeClassTuple] = [
            ParentNodeClassTuple(
                nodes.topic,
                ["p", ""],
                {"CLASS": "topic-title first"},
                None,
            ),
            ParentNodeClassTuple(
                nodes.sidebar,
                ["p", ""],
                {"CLASS": "sidebar-title"},
                None,
            ),
            ParentNodeClassTuple(
                nodes.Admonition,
                ["p", ""],
                {"CLASS": "admonition-title"},
                None,
            ),
            ParentNodeClassTuple(nodes.table, ["caption", ""], {}, "</caption>"),
        ]

        # if node is wrapped in a certain type and processed, toggle this
        is_processed = False

        for parent_node_class in parent_node_classes:
            if isinstance(node.parent, parent_node_class.parent_node_type):
                self.body.append(
                    self.starttag(
                        node,
                        *parent_node_class.args,
                        **parent_node_class.kwargs,
                    ),
                )
                if close_tag:
                    close_tag = parent_node_class.close_tag
                is_processed = True

        # if one of the specific nodes already appended tag, don't re-run
        # since we used a for loop above, we can't elif this
        if not is_processed:
            if isinstance(node.parent, nodes.document):
                self.body.append(self.starttag(node, "h1", "", CLASS="title is-1"))
                close_tag = "</h1>\n"
                self.in_document_title = len(self.body)
            elif isinstance(node.parent, nodes.section):
                # now, handle plain-old headers
                # this is pretty verbose, break it off into another method
                close_tag = self._visit_section_title(node, close_tag)

        self.context.append(close_tag)

    def _visit_section_title(
        self,
        node: nodes.Element,
        close_tag: t.Optional[str],
    ) -> str:
        """Our special sauce for section titles.

        Extracted from :meth:`.visit_title` to reduce complexity.

        Parameters
        ----------
        node : :class:`docutils.nodes.title`
            Title node being visited
        close_tag : str
            Close tag (passed in from visit_title)

        Returns
        -------
        str
            Close tag for section title node.
        """
        h_level = self.section_level + self.initial_header_level - 1
        atts: t.Dict[str, str] = {}
        if len(node.parent) >= 2 and isinstance(node.parent[1], nodes.subtitle):
            atts["CLASS"] = "subtitle"

        self.body.append(self.starttag(node, "h%s" % h_level, "", **atts))
        attrs: t.Dict[str, str] = {}
        if node.hasattr("refid"):
            attrs["class"] = "toc-backref"
            attrs["href"] = "#" + node["refid"]
        if attrs:
            self.body.append(self.starttag({}, "a", "", **attrs))  # type:ignore
            close_tag = f"</a></h{h_level}>\n"
        else:
            close_tag = f"</h{h_level}>\n"
        return close_tag

    def visit_docinfo(self, node: nodes.Element) -> None:
        """Skip docinfo."""
        raise nodes.SkipNode

    def visit_icon(self, node: nodes.decoration) -> None:
        """Open <em> tag."""
        atts = {}
        if "style" in node:
            atts["style"] = node["style"]
        self.body.append(self.starttag(node, "em", "", **atts))

    def depart_icon(self, node: nodes.decoration) -> None:
        """Close <em> tag."""
        self.body.append("</em>")


class DjangoDocutilsWriter(Writer):
    """DjangoDocutils's hand-crafted docutils' writer.

    Example:

    >>> DJANGO_DOCUTILS_LIB_RST = {
    ...    'transforms': [  #: docutils.transforms.Transform class (import string)
    ...        'django_docutils.lib.transforms.xref.XRefTransform'
    ...    ]
    ... }
    """

    def __init__(self) -> None:
        Writer.__init__(self)
        # I'd like to put this into the class attribute, but I think
        # somewhere up the Writer/Translator hierarchy are 'old' python
        # classes. (e.g. Python =< 2.1 classes)
        self.translator_class = DjangoDocutilsHTMLTranslator

    def get_transforms(self) -> list[t.Type[Transform]]:
        """Return transformed required by DjangoDocutilsWriter.

        Adheres to DJANGO_DOCUTILS_LIB_RST settings.
        """
        transforms = Writer.get_transforms(self)

        if not DJANGO_DOCUTILS_LIB_RST:
            return transforms

        if "transforms" in DJANGO_DOCUTILS_LIB_RST:
            for transforms_cls_str in DJANGO_DOCUTILS_LIB_RST["transforms"]:
                transforms += [import_string(transforms_cls_str)]

        return transforms
