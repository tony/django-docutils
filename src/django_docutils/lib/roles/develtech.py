from django.urls import NoReverseMatch, reverse
from docutils import nodes, utils

from ..utils import split_explicit_title


def site_url_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
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


def post_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    from django.apps import apps

    from django_docutils.lib.fixtures.utils import get_model_from_post_app

    # split :post:appname:`post_id` into :post:appname:
    raw_role = rawtext.split("`")[0]

    app_name_singular = raw_role.split(":")[2]
    app_config = apps.get_app_config(f"{app_name_singular}s")
    Model = get_model_from_post_app(app_config)

    name = name.lower()
    has_explicit_title, title, target = split_explicit_title(text)
    title = utils.unescape(title)
    target = utils.unescape(target)

    try:
        obj = Model.objects.get(slug_id=target)
        url = obj.get_absolute_url()
        if not has_explicit_title:
            title = obj.title
    except (Model.DoesNotExist, NoReverseMatch) as e:
        msg = inliner.reporter.error(f"{e} ({target})", line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    sn = nodes.Text(title, title)
    rn = nodes.reference("", "", internal=True, refuri=url, classes=[name])
    rn += sn
    return [rn], []
