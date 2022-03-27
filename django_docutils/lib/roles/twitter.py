from .common import generic_url_role


def twitter_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for linking to twitter articles.

    :twitter:`@username` ->
       link: https://twitter.com/username
       text: @username

    :twitter:`follow me on twitter <@username>` ->
       link: https://twitter.com/username
       text: follow on me on twitter
    """

    def url_handler(target):
        if "@" in target:
            target = target.replace("@", "")

        return f"https://twitter.com/{target}"

    return generic_url_role(name, text, url_handler)
