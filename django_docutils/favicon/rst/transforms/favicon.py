import tldextract
from django.db.models import Q
from docutils import nodes
from docutils.transforms import Transform

from django_docutils.favicon.models import get_favicon_model

from ..nodes import icon

Favicon = get_favicon_model()


def resolve_favicon(url):
    """Given a URL to a website, see if a Favicon exists in db.

    URL will be resolved to a fqdn for a key lookup.

    :param url: URL to any page on a website
    :type url: str
    :returns: Full Storage based favicon url path, or None
    :rtype: str|None
    """
    # e.g. forums.bbc.co.uk
    fqdn = tldextract.extract(url).fqdn

    try:
        return Favicon.objects.get(domain=fqdn).favicon.url
    except (ValueError, Favicon.DoesNotExist):
        return None


class FaviconTransform(Transform):
    #: run after based.app.references.rst.transforms.xref
    default_priority = 20

    def apply(self):
        q = Q()

        # first run, iterate through references, extract FQDN's, add to query
        for node in self.document.traverse(plain_references):
            q.add(Q(domain__exact=tldextract.extract(node["refuri"]).fqdn), Q.OR)

        # pull all fqdn's with a favicon
        favicons = Favicon.objects.filter(q)

        for node in self.document.traverse(plain_references):
            fqdn = tldextract.extract(node["refuri"]).fqdn
            try:
                favicon_url = next(  # Find favicon matching fqdn
                    (f.favicon.url for f in favicons if f.domain == fqdn), None
                )
            except ValueError:  # no favicon exists for fqdn
                favicon_url = None

            if favicon_url:
                nodecopy = node.deepcopy()
                ico = icon(
                    "",
                    "",
                    style=f"background-image: url({favicon_url})",
                    classes=["ico"],
                )
                nodecopy.insert(0, ico)
                node.replace_self(nodecopy)


def plain_references(node):
    """Docutils traversal: Only return references with URI's, skip xref's

    If a nodes.reference already has classes, it's an icon class from xref,
    so skip that.

    If a nodes.reference has no 'refuri', it's junk, skip.

    Docutils node.traverse condition callback

    :returns: True if it's a URL we want to lookup favicons for
    :rtype: bool
    """
    if isinstance(node, nodes.reference):
        # skip nodes already with xref icon classes or no refuri
        no_classes = "classes" not in node or not node["classes"]
        has_refuri = "refuri" in node
        if no_classes and has_refuri and node["refuri"].startswith("http"):
            return True
    return False
