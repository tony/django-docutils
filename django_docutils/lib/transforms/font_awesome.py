import re

from docutils import nodes, utils
from docutils.transforms import Transform

from django_docutils.lib.settings import BASED_LIB_RST

url_patterns = BASED_LIB_RST.get("font_awesome", {}).get("url_patterns", {})
permissible_nodes = [nodes.Text]


def fa_classes_from_url(url: str) -> str:
    for url_pattern, classes in url_patterns.items():
        if re.match(url_pattern, url):

            return classes

    return ""


def inject_font_awesome_to_ref_node(target: nodes.Node, url: str):
    fa_classes = fa_classes_from_url(url=url)
    if fa_classes != "":
        fa_tag = f'<em class="{fa_classes}"></em>'
        title = utils.unescape(target[0])
        rn = nodes.reference("", "", internal=True, refuri=url)
        rn += nodes.raw("", fa_tag, format="html")
        rn += target[0].__class__(title, title)
        return rn
    return None


class InjectFontAwesome(Transform):

    default_priority = 680

    def apply(self):
        for target in self.document.traverse(nodes.reference):
            if target.hasattr("refuri") and any(
                isinstance(target[0], node_type) for node_type in permissible_nodes
            ):
                rn = inject_font_awesome_to_ref_node(
                    target=target, url=target["refuri"]
                )
                if rn is not None:
                    target.replace_self(rn)
