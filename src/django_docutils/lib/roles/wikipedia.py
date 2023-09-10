from urllib.parse import quote

from .common import generic_url_role


def wikipedia_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """Role for linking to Wikipedia articles.

    :wikipedia:`Don't repeat yourself` ->
       link: https://en.wikipedia.org/wiki/Don%27t_repeat_yourself
       text: Don't repeat yourself


    :wikipedia:`this wikipedia article <vim-airline>` ->
       link: https://github.com/vim-airline
       text: this wikipedia article
    """

    if content is None:
        content = []
    if options is None:
        options = {}
    def url_handler(target):
        target = quote(target.replace(" ", "_"))
        return f"https://en.wikipedia.org/wiki/{target}"

    return generic_url_role(name, text, url_handler)
