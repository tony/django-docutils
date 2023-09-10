from .common import generic_url_role


def email_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """Role for linking to email articles.

    :email:`me@localhost` ->
       link: mailto:me@localhost
       text: me@localhost

    :email:`E-mail me <me@localhost>` ->
       link: mailto:me@localhost
       text: E-mail me

    """

    if content is None:
        content = []
    if options is None:
        options = {}

    def url_handler(target):
        return f"mailto:{target}"

    return generic_url_role(name, text, url_handler)
