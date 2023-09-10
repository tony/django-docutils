from .common import generic_url_role


def twitter_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """Role for linking to twitter articles.

    :twitter:`@username` ->
       link: https://twitter.com/username
       text: @username

    :twitter:`follow me on twitter <@username>` ->
       link: https://twitter.com/username
       text: follow on me on twitter
    """

    if content is None:
        content = []
    if options is None:
        options = {}

    def url_handler(target):
        if "@" in target:
            target = target.replace("@", "")

        return f"https://twitter.com/{target}"

    return generic_url_role(name, text, url_handler)
