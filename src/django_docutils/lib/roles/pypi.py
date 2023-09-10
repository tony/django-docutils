from .common import generic_url_role


def pypi_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """Role for linking to pypi page.

    :pypi:`libsass` ->
       link: https://pypi.python.org/pypi/libsass
       text: libsass


    :pypi:`a pypi package <libsass>` ->
       link: https://pypi.python.org/pypi/libsass
       text: a pypi package
    """

    if content is None:
        content = []
    if options is None:
        options = {}

    def url_handler(target):
        return f"https://pypi.python.org/pypi/{target}"

    return generic_url_role(name, text, url_handler)
