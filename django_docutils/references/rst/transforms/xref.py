from os import path

from django.utils.translation import gettext_lazy as _
from docutils import nodes
from docutils.transforms import Transform
from docutils.utils import relative_path

from django_docutils.lib.transforms.font_awesome import fa_classes_from_url
from django_docutils.references.models import get_reference_model

from ..nodes import pending_xref

Reference = get_reference_model()


class XRefTransform(Transform):
    default_priority = 5

    def apply(self):
        references = Reference.objects.all().values()

        for node in self.document.traverse(pending_xref):
            contnode = node[0].deepcopy()
            domain = "std"
            project, target = node["reftarget"].split(":", 1)

            ref = next(
                (
                    r
                    for r in references
                    if r["target"] == target and r["project"] == project
                ),
                None,
            )

            if not ref:
                ref = next((r for r in references if r["target"] == target), None)

            proj, version, uri, dispname = (
                ref["project"],
                ref["project_version"],
                ref["uri"],
                ref["display_name"],
            )

            if not dispname:
                dispname = "-"
            if "://" not in uri and node.get("refdoc"):
                # get correct path in case of subdirectories
                uri = path.join(relative_path(node["refdoc"], "."), uri)
            newnode = nodes.reference(
                "",
                "",
                internal=False,
                refuri=uri,
                reftitle=_("(in %s v%s)") % (proj, version),
            )

            if node.get("refexplicit"):
                # use whatever title was given
                newnode.append(contnode)
            elif dispname == "-" or (domain == "std" and node["reftype"] == "keyword"):
                # use whatever title was given, but strip prefix
                title = contnode.astext()
                if project and title.startswith(project + ":"):
                    newnode.append(
                        contnode.__class__(
                            title[len(project) + 1 :], title[len(project) + 1 :]
                        )
                    )
                else:
                    newnode.append(contnode)
            else:
                # else use the given display name (used for :ref:)
                newnode.append(contnode.__class__(dispname, dispname))

            fa_classes = fa_classes_from_url(url=uri)
            if fa_classes != "":
                fa_tag = f'<em class="{fa_classes}"></em>'
                newnode.insert(0, nodes.raw("", fa_tag, format="html"))

            node.replace_self(newnode)

    def visit_pending_xref(self, node):
        pass

    def depart_pending_xref(self, node):
        pass
