import sys

from docutils import nodes
from docutils.transforms import parts


class Contents(parts.Contents):

    """
    Changes:
    - remove unused autonum
    - PEP8
    - Removed extra nodes.paragraph wrapping of list_item's
    """

    def build_contents(self, node, level=0):
        level += 1
        sections = [sect for sect in node if isinstance(sect, nodes.section)]
        entries = []
        depth = self.startnode.details.get("depth", sys.maxsize)

        for section in sections:
            title = section[0]
            auto = title.get("auto")  # May be set by SectNum.
            entrytext = self.copy_and_filter(title)
            reference = nodes.reference("", "", refid=section["ids"][0], *entrytext)
            ref_id = self.document.set_id(reference)
            item = nodes.list_item("", reference)
            if (
                self.backlinks in ("entry", "top")
                and title.next_node(nodes.reference) is None
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
