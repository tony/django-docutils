"""
ported from sphinx.ext.intersphinx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Insert links to objects documented in remote Sphinx documentation.

This works as follows:

* Each Sphinx HTML build creates a file named "objects.inv" that contains a
    mapping from object names to URIs relative to the HTML set's root.

* Projects using the Intersphinx extension can specify links to such
    mapping files in the `intersphinx_mapping` config value.  The mapping
    will then be used to resolve otherwise missing references to objects into
    links to the other documentation.

* By default, the mapping file is assumed to be at the same location as the
    rest of the documentation; however, the location of the mapping file can
    also be specified individually, e.g. if the docs should be buildable
    without Internet access.

:copyright: Copyright 2007-2017 by the Sphinx team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""
import functools
import posixpath
from os import path

import requests
from six import PY3
from six.moves.urllib.parse import urlsplit, urlunsplit
from tqdm import trange

from django_docutils.references.models import get_reference_model

from .utils import InventoryFile

Reference = get_reference_model()
intersphinx_cache_limit = 5
intersphinx_timeout = None
INVENTORY_FILENAME = "objects.inv"

if False:
    # For type annotation
    from typing import IO, Any, Dict, List, Tuple, Union  # NOQA

    from sphinx import Config, Sphinx

    if PY3:
        unicode = str

    Inventory = Dict[unicode, Dict[unicode, Tuple[unicode, unicode, unicode, unicode]]]

intersphinx_mapping = {
    "python": ("https://docs.python.org/2/", None),
    "django": (
        "https://docs.djangoproject.com/en/1.11/",
        "https://docs.djangoproject.com/en/1.11/_objects/",
    ),
    "flask": ("http://flask.pocoo.org/docs/", None),
    "flask-sqlalchemy": ("http://flask-sqlalchemy.pocoo.org/2.2/", None),
    "werkzeug": ("http://werkzeug.pocoo.org/docs/0.12/", None),
    "jinja": ("http://jinja.pocoo.org/docs/dev", None),
    "sqlalchemy": ("http://docs.sqlalchemy.org/en/latest/", None),
    "uwsgi": ("https://uwsgi-docs.readthedocs.io/en/latest/", None),
}


class InventoryAdapter:

    """Inventory adapter for environment"""

    def __init__(self, env):
        self.env = env

        if not hasattr(env, "intersphinx_cache"):
            self.env.intersphinx_cache = {}
            self.env.intersphinx_inventory = {}
            self.env.intersphinx_named_inventory = {}

    @property
    def cache(self):
        # type: () -> Dict[unicode, Tuple[unicode, int, Inventory]]
        return self.env.intersphinx_cache

    @property
    def main_inventory(self):
        # type: () -> Inventory
        return self.env.intersphinx_inventory

    @property
    def named_inventory(self):
        # type: () -> Dict[unicode, Inventory]
        return self.env.intersphinx_named_inventory

    def clear(self):
        self.env.intersphinx_inventory.clear()
        self.env.intersphinx_named_inventory.clear()


def _strip_basic_auth(url):
    # type: (unicode) -> unicode
    """Returns *url* with basic auth credentials removed. Also returns the
    basic auth username and password if they're present in *url*.

    E.g.: https://user:pass@example.com => https://example.com

    *url* need not include basic auth credentials.

    :param url: url which may or may not contain basic auth credentials
    :type url: ``str``

    :return: *url* with any basic auth creds removed
    :rtype: ``str``
    """
    frags = list(urlsplit(url))
    # swap out "user[:pass]@hostname" for "hostname"
    if "@" in frags[1]:
        frags[1] = frags[1].split("@")[1]
    return urlunsplit(frags)


def _read_from_url(url, requests_config={}, intersphinx_timeout=intersphinx_timeout):
    # type: (unicode, Config) -> IO
    """Reads data from *url* with an HTTP *GET*.

    This function supports fetching from resources which use basic HTTP auth as
    laid out by RFC1738 § 3.1. See § 5 for grammar definitions for URLs.

    .. seealso:

       https://www.ietf.org/rfc/rfc1738.txt

    :param url: URL of an HTTP resource
    :type url: ``str``

    :return: data read from resource described by *url*
    :rtype: ``file``-like object
    """
    r = requests.get(
        url,
        stream=True,
        # config=requests_config,
        timeout=intersphinx_timeout,
    )
    r.raise_for_status()
    r.raw.url = r.url
    # decode content-body based on the header.
    # ref: https://github.com/kennethreitz/requests/issues/2155
    r.raw.read = functools.partial(r.raw.read, decode_content=True)
    return r.raw


def _get_safe_url(url):
    # type: (unicode) -> unicode
    """Gets version of *url* with basic auth passwords obscured. This function
    returns results suitable for printing and logging.

    E.g.: https://user:12345@example.com => https://user@example.com

    :param url: a url
    :type url: ``str``

    :return: *url* with password removed
    :rtype: ``str``
    """
    parts = urlsplit(url)
    if parts.username is None:
        return url
    else:
        frags = list(parts)
        if parts.port:
            frags[1] = f"{parts.username}@{parts.hostname}:{parts.port}"
        else:
            frags[1] = f"{parts.username}@{parts.hostname}"

        return urlunsplit(frags)


def fetch_inventory(uri, inv, srcdir=None, requests_config={}):  # NOQA: C901
    # type: (Sphinx, unicode, Any) -> Any
    """Fetch, parse and return an intersphinx inventory file."""
    # both *uri* (base URI of the links to generate) and *inv* (actual
    # location of the inventory file) can be local or remote URIs
    localuri = "://" not in uri
    if not localuri:
        # case: inv URI points to remote resource; strip any existing auth
        uri = _strip_basic_auth(uri)
    try:
        if "://" in inv:
            f = _read_from_url(inv, requests_config=requests_config)
        else:
            f = open(path.join(srcdir, inv), "rb")
    except Exception as err:
        print(
            "intersphinx inventory %r not fetchable due to %s: %s",
            inv,
            err.__class__,
            err,
        )
        return
    try:
        if hasattr(f, "url"):
            newinv = f.url  # type: ignore
            if inv != newinv:
                print("intersphinx inventory has moved: %s -> %s", inv, newinv)

                if uri in (inv, path.dirname(inv), path.dirname(inv) + "/"):
                    uri = path.dirname(newinv)
        with f:
            try:
                join = localuri and path.join or posixpath.join
                invdata = InventoryFile.load(f, uri, join)
            except ValueError as exc:
                raise ValueError("unknown or unsupported inventory version: %r" % exc)
    except Exception as err:
        print(
            "intersphinx inventory %r not readable due to %s: %s",
            inv,
            err.__class__.__name__,
            err,
        )
    else:
        return invdata


def load_mappings():  # NOQA: C901
    # type: (Sphinx) -> None
    inventories = {}
    """Load all intersphinx mappings into the environment."""
    for key, value in intersphinx_mapping.items():
        name = None  # type: unicode
        uri = None  # type: unicode
        inv = None  # type: Union[unicode, Tuple[unicode, ...]]

        if isinstance(value, (list, tuple)):
            # new format
            name, (uri, inv) = key, value  # type: ignore
            if not isinstance(name, str):
                print("intersphinx identifier %r is not string. Ignored", name)
                continue
        else:
            # old format, no name
            name, uri, inv = None, key, value
        # we can safely assume that the uri<->inv mapping is not changed
        # during partial rebuilds since a changed intersphinx_mapping
        # setting will cause a full environment reread
        if not isinstance(inv, tuple):
            invs = (inv,)
        else:
            invs = inv  # type: ignore

        for inv in invs:
            if not inv:
                inv = posixpath.join(uri, INVENTORY_FILENAME)
            # decide whether the inventory must be read: always read local
            # files; remote ones only if the cache time is expired
            safe_inv_url = _get_safe_url(inv)  # type: ignore
            print("loading intersphinx inventory from %s..." % safe_inv_url)
            invdata = fetch_inventory(uri, inv)
            if invdata:
                inventories[uri] = (name, invdata)
                break

    # Duplicate values in different inventories will shadow each
    # other; which one will override which can vary between builds
    # since they are specified using an unordered dict.  To make
    # it more consistent, we sort the named inventories and then
    # add the unnamed inventories last.  This means that the
    # unnamed inventories will shadow the named ones but the named
    # ones can still be accessed when the name is specified.
    named_vals = sorted(v for v in list(inventories.values()) if v[0])

    to_insert = []
    references = list(Reference.objects.all().values())

    def reference_is_match(record_values, inventory_values, keys):
        try:
            for key in keys:
                if record_values[key] != inventory_values[key]:
                    return False
        except KeyError:
            return False
        return True

    def reference_is_full_match(record_values, inventory_values):
        """If these do not match, we need an update."""
        for k, v in inventory_values.items():
            ok = (k, v) in record_values.items()
            if not ok:
                print(f"item {k}, {v} not in records ({record_values})")
                return False
        return True

    combined_inventory = []
    # merge them all into a big ass list
    for project, invdata in named_vals:
        for domain_and_type, invdata2 in invdata.items():
            domain, type_ = domain_and_type.split(":")
            for target, values in invdata2.items():
                proj, version, uri, dispname = values
                combined_inventory.append(
                    {
                        "domain": domain,
                        "type": type_,
                        "project": project,
                        "project_version": version,
                        "target": target,
                        "uri": uri,
                        "display_name": dispname,
                    }
                )

    t = trange(len(combined_inventory))
    for item in combined_inventory:
        t.update(1)
        r = next(
            (
                ref
                for ref in references
                if reference_is_match(ref, item, ["target", "project", "type"])
            ),
            None,
        )

        if r and r in references:
            references.remove(r)

        if r and not reference_is_full_match(r, item):
            # these are records that need updating
            pass

        # TODO, add this to a to_update list
        # r = rqueryset.get(
        #     domain=domain,
        #     type=_type,
        #     project=name,
        #     project_version=version,
        #     target=target
        # )
        #
        # if r.uri != uri:
        #     r.uri = uri
        #     r.save()
        # if r.display_name != dispname:
        #     r.display_name = dispname
        #     r.save()
        if not r:
            r = Reference(
                domain=item["domain"],
                type=item["type"],
                project=item["project"],
                project_version=item["project_version"],
                target=item["target"],
                uri=item["uri"],
                display_name=item["display_name"],
            )
            to_insert.append(r)

    if len(to_insert):
        Reference.objects.bulk_create(to_insert)
