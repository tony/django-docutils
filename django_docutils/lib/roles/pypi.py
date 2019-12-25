from .common import generic_url_role


def pypi_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for linking to pypi page.

    :pypi:`libsass` ->
       link: https://pypi.python.org/pypi/libsass
       text: libsass


    :pypi:`a pypi package <libsass>` ->
       link: https://pypi.python.org/pypi/libsass
       text: a pypi package
    """

    def url_handler(target):
        return f'https://pypi.python.org/pypi/{target}'

    return generic_url_role(name, text, url_handler)
