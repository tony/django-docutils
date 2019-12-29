from docutils import nodes, utils

from ..utils import split_explicit_title


def generic_url_role(name, text, url_handler_fn, innernodeclass=nodes.Text):
    """This cleans up a lot of code we had to repeat over and over.

    This generic role also handles explicit titles (:role:`yata yata <target>`)

    This breaks convention a feels a bit jenky at first. It uses a callback
    because figuring out the url is the only magic that happens, but its
    sandwiched in the middle.

    :param name: name of the role, e.g. 'github'
    :type name: string
    :param text: text inside of the role, e.g:
        - 'airline-mode/airline-mode'
        - 'this repo <airline-mode/airline-mode>'
    :type text: string
    :param url_handler_fn: a function that accepts the target param, example:
    :returntype url_handler_fn: string
    :returns: tuple ([node], [])
    :returntype: tuple

    Simple example, let's create a role::

    .. code-block:: python

        def github_role(
            name, rawtext, text, lineno, inliner, options={}, content=[]
        ):
            def url_handler(target):
                return 'https://github.com/{}'.format(target)

            return generic_url_role(name, text, url_handler)

        roles.register_local_role('gh', github_role)
    """
    name = name.lower()
    has_explicit_title, title, target = split_explicit_title(text)
    title = utils.unescape(title)
    target = utils.unescape(target)

    if not has_explicit_title:
        title = utils.unescape(title)
    else:
        if '**' == title[:2] and '**' == title[-2:]:
            innernodeclass = nodes.strong
            title = title.strip('**')
        elif '*' == title[0] and '*' == title[-1]:
            innernodeclass = nodes.emphasis
            title = title.strip('*')

    url = url_handler_fn(target)

    sn = innernodeclass(title, title)
    rn = nodes.reference('', '', internal=True, refuri=url, classes=[name])
    rn += sn
    return [rn], []


def generic_remote_url_role(name, text, url_handler_fn, innernodeclass=nodes.Text):
    """This is a generic_url_role that can return a url AND a title remotely

    The url_handler_fn returns a title and a url

    In cases like Amazon API, database lookups, and other stuff, information
    may be looked up by key, and we may get a fresh title to fill in if nothing
    else explicit is mentioned.

    :param name: name of the role, e.g. 'github'
    :type name: string
    :param text: text inside of the role, e.g:
        - 'airline-mode/airline-mode'
        - 'this repo <airline-mode/airline-mode>'
    :type text: string
    :param url_handler_fn: a function that accepts the target param, example:
    :returntype url_handler_fn: (string, string)
    :returns: tuple ([node], [])
    :returntype: tuple

    Simple example, let's create a role::

    .. code-block:: python

        def amzn_role(
            name, rawtext, text, lineno, inliner, options={}, content=[]
        ):
            def url_handler(target):
                query = amzn.lookup(ItemId=target)
                return query.title, query.offer_url

            return generic_remote_url_role(name, text, url_handler)

        roles.register_local_role('amzn', amzn_role)
    """
    name = name.lower()
    has_explicit_title, title, target = split_explicit_title(text)
    title = utils.unescape(title)
    target = utils.unescape(target)

    remote_title, url = url_handler_fn(target)
    if not has_explicit_title:
        title = utils.unescape(remote_title)

    sn = innernodeclass(title, title)
    rn = nodes.reference('', '', internal=True, refuri=url, classes=[name])
    rn += sn
    return [rn], []
