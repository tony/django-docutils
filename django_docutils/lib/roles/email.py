from .common import generic_url_role


def email_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for linking to email articles.

    :email:`me@localhost` ->
       link: mailto:me@localhost
       text: me@localhost

    :email:`E-mail me <me@localhost>` ->
       link: mailto:me@localhost
       text: E-mail me

    """

    def url_handler(target):
        return f'mailto:{target}'

    return generic_url_role(name, text, url_handler)
