from .common import generic_url_role


def leanpub_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """Role for linking to leanpub page.

    :leanpub:`the-tao-of-tmux` ->
       link: https://leanpub.com/the-tao-of-tmux
       text: the-tao-of-tmux

    :leanpub:`my book <the-tao-of-tmux>` ->
       link: https://leanpub.com/the-tao-of-tmux
       text: my book

    :leanpub:`The Tao of tmux <the-tao-of-tmux:read>` ->
       link: https://leanpub.com/the-tao-of-tmux/read
       text: The Tao of tmux
    """

    if content is None:
        content = []
    if options is None:
        options = {}

    def url_handler(target):
        if ":" in target:
            project, path = target.split(":")
            return f"https://leanpub.com/{project}/{path}"
        return f"https://leanpub.com/{target}"

    return generic_url_role(name, text, url_handler)
