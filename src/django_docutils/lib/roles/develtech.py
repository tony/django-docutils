from django.urls import NoReverseMatch, reverse
from docutils import nodes, utils

from ..utils import split_explicit_title


def site_url_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    if content is None:
        content = []
    if options is None:
        options = {}
    name = name.lower()

    has_explicit_title, title, target = split_explicit_title(text)
    title = utils.unescape(title)
    target = utils.unescape(target)

    if not has_explicit_title:
        title = "Page " + utils.unescape(title)
    try:
        url = reverse(target)
    except NoReverseMatch:
        msg = inliner.reporter.error("no matching url %s" % target, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    sn = nodes.Text(title, title)
    rn = nodes.reference("", "", internal=True, refuri=url, classes=[name])
    rn += sn
    return [rn], []
