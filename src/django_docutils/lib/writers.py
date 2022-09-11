from django.conf import settings
from django.utils.module_loading import import_string
from docutils import nodes
from docutils.writers.html5_polyglot import HTMLTranslator, Writer

from .settings import BASED_LIB_RST


class BasedHTMLTranslator(HTMLTranslator):
    def __init__(self, document):
        HTMLTranslator.__init__(self, document)

    def visit_pending_xref(self, node):
        pass

    def depart_pending_xref(self, node):
        pass

    def visit_table(self, node):
        node["classes"].extend(["table"])
        HTMLTranslator.visit_table(self, node)

    def visit_reference(self, node):
        """
        Changes:

        - monkeypatch bugfix https://sourceforge.net/p/docutils/bugs/322/
        - add target _blank to offsite urls
        - add class offsite for offsite urls
        - add class insite for insite urls (note, internal is already used
          for reference links in the *same* document)
        """
        atts = {"class": "reference"}

        if "refuri" in node:
            atts["href"] = node["refuri"]
            if self.settings.cloak_email_addresses and atts["href"].startswith(
                "mailto:"
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

        from django_docutils.favicon.rst.nodes import icon

        if isinstance(node[0], icon):
            atts["class"] = ""
        self.body.append(self.starttag(node, "a", "", **atts))

    def visit_title(self, node):
        """Changes:
        - add backlinks for Contents refid headers
          since they are baked inside the Section (parent) of the anchor
          since we're using an ad-hoc contents transformation process
          that builds toc separately from the main content (see templatetags)
        - s/with-subtitle/subtitle for bulma css
        """
        close_tag = "</p>\n"

        # add backlinks to refid (toc header backlinks)
        # This assures headers link to themselves, so users can copy a link
        # to the anchor, rather than docutils default behavior of linking back
        # to the doc
        if isinstance(node.parent, nodes.section):
            node["refid"] = node.parent["ids"][0]

        # specific cases we don't use h{1-6} tags for
        parent_node_classes = [
            (nodes.topic, ["p", ""], {"CLASS": "topic-title first"}, None),
            (nodes.sidebar, ["p", ""], {"CLASS": "sidebar-title"}, None),
            (nodes.Admonition, ["p", ""], {"CLASS": "admonition-title"}, None),
            (nodes.table, ["caption", ""], {}, "</caption>"),
        ]

        # if node is wrapped in a certain type and processed, toggle this
        is_processed = False

        for parent_node_type, args, kwargs, close_tag in parent_node_classes:
            if isinstance(node.parent, parent_node_type):
                self.body.append(self.starttag(node, *args, **kwargs))
                if close_tag:
                    close_tag = close_tag
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

    def _visit_section_title(self, node, close_tag):
        """Our special sauce for section titles.

        We broke this off to reduce complexity.

        :param node: title node being visited
        :type node: :class:`docutils.nodes.title`
        :param close_tag: close tag (passed in from visit_title)
        :type close_tag str
        :rtype: str
        :returns: close_tag
        """
        h_level = self.section_level + self.initial_header_level - 1
        atts = {}
        if len(node.parent) >= 2 and isinstance(node.parent[1], nodes.subtitle):
            atts["CLASS"] = "subtitle"

        self.body.append(self.starttag(node, "h%s" % h_level, "", **atts))
        atts = {}
        if node.hasattr("refid"):
            atts["class"] = "toc-backref"
            atts["href"] = "#" + node["refid"]
        if atts:
            self.body.append(self.starttag({}, "a", "", **atts))
            close_tag = "</a></h%s>\n" % (h_level)
        else:
            close_tag = "</h%s>\n" % (h_level)
        return close_tag

    def visit_docinfo(self, node):
        # type: (nodes.Node) -> None
        raise nodes.SkipNode

    def visit_icon(self, node):
        atts = {}
        if "style" in node:
            atts["style"] = node["style"]
        self.body.append(self.starttag(node, "em", "", **atts))

    def depart_icon(self, node):
        self.body.append("</em>")


class BasedWriter(Writer):

    """Based's hand-crafted docutils' writer::

    BASED_LIB_RST = {
        'transforms': [  #: docutils.transforms.Transform class (import string)
            'django_docutils.lib.transforms.xref.XRefTransform'
        ]
    }
    """

    def __init__(self):
        Writer.__init__(self)
        # I'd like to put this into the class attribute, but I think
        # somewhere up the Writer/Translator hierarchy are 'old' python
        # classes. (e.g. Python =< 2.1 classes)
        self.translator_class = BasedHTMLTranslator

    def get_transforms(self):
        transforms = Writer.get_transforms(self)

        if not BASED_LIB_RST:
            return transforms

        if "transforms" in BASED_LIB_RST:
            for transforms_cls_str in BASED_LIB_RST["transforms"]:
                transforms += [import_string(transforms_cls_str)]

        return transforms
