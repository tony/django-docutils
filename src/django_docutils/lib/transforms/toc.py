"""Django docutils table of contents helpers."""
import sys
import typing as t

from docutils import nodes
from docutils.transforms import parts


class Contents(parts.Contents):
    """Helpers for rendering docutils table of contents from document tree.

    Changes:
    - Remove unused autonum
    - PEP8
    - Removed extra nodes.paragraph wrapping of list_item's.
    """

    startnode: t.Optional[nodes.Node]

    def build_contents(
        self, node: nodes.Node, level: int = 0
    ) -> t.Union[nodes.bullet_list, list[t.Any]]:
        """Build nested bullet list from doctree content."""
        assert isinstance(node, nodes.Element)
        level += 1
        sections: list[nodes.section] = [
            sect for sect in node.children if isinstance(sect, nodes.section)
        ]
        assert self.startnode is not None
        entries: list[nodes.Node] = []

        depth = (
            self.startnode.details.get("depth", sys.maxsize)
            if hasattr(self.startnode, "details")
            else sys.maxsize
        )
        auto = False

        for section in sections:
            title = section[0]
            auto = (
                title.get("auto") if hasattr(title, "get") else False
            )  # May be set by SectNum.
            entrytext = self.copy_and_filter(title)
            reference = nodes.reference(
                "",
                "",
                refid=section["ids"][0],
                *entrytext,  # noqa: B026
            )
            ref_id = self.document.set_id(reference)
            item = nodes.list_item("", reference)
            if (
                self.backlinks in ("entry", "top")
                and title.next_node(nodes.reference) is None
                and isinstance(title, (nodes.Element, nodes.TextElement))
            ):
                if self.backlinks == "entry":
                    title["refid"] = ref_id
                elif self.backlinks == "top":
                    title["refid"] = self.toc_id
            if level < depth:
                subsects = self.build_contents(section, level)
                item += subsects
            entries.append(item)
        if entries:
            contents = nodes.bullet_list("", *entries, classes=["menu-list"])

            if auto:
                contents["classes"].append("auto-toc")
            return contents
        else:
            return []
