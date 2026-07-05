"""Sphinx configuration for Django Docutils."""

from __future__ import annotations

import os
import pathlib
import sys

import django
from gp_sphinx.config import make_linkcode_resolve, merge_sphinx_config

import django_docutils

# Get the project root dir, which is the parent dir of this
cwd = pathlib.Path(__file__).parent
project_root = cwd.parent
src_root = project_root / "src"

sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_root))

os.environ["DJANGO_SETTINGS_MODULE"] = "django_docutils.lib.settings"
django.setup()

# package data
about: dict[str, str] = {}
with (src_root / "django_docutils" / "__about__.py").open() as fp:
    exec(fp.read(), about)

conf = merge_sphinx_config(
    project=about["__title__"],
    version=about["__version__"],
    copyright=about["__copyright__"],
    source_repository=f"{about['__github__']}/",
    docs_url=about["__docs__"],
    source_branch="master",
    light_logo="img/icons/logo.svg",
    dark_logo="img/icons/logo-dark.svg",
    extra_extensions=[
        "sphinx.ext.doctest",
        "sphinx_autodoc_api_style",
        "sphinx_autodoc_docutils",
        "sphinx_autodoc_sphinx",
        "sphinx_click.ext",
    ],
    intersphinx_mapping={
        "python": ("http://docs.python.org/", None),
        "django": (
            "https://docs.djangoproject.com/en/6.1/",
            "https://docs.djangoproject.com/en/6.1/_objects/",
        ),
    },
    linkcode_resolve=make_linkcode_resolve(django_docutils, about["__github__"]),
    html_favicon="_static/favicon.ico",
    html_extra_path=["manifest.json"],
    rediraffe_redirects="redirects.txt",
    autodoc_mock_imports=["django"],
    set_type_checking_flag=True,
    # AGENTS.md is agent guidance, not a site page; keep Sphinx from
    # treating it as an orphan document.
    exclude_patterns=["_build", "AGENTS.md", "CLAUDE.md"],
)
globals().update(conf)

doctest_global_setup = """
from docutils import nodes
from django_docutils.lib.publisher import (
    publish_doctree,
    publish_html_from_doctree,
    publish_html_from_source,
    publish_parts_from_doctree,
)
from django_docutils.lib.roles.kbd import kbd_role
from django_docutils.lib.sanitize import (
    SanitizeTransform,
    _remove_node,
    _replace_node_with_text,
    _uri_is_allowed,
    sanitize_doctree,
)
from django_docutils.lib.settings import (
    DJANGO_DOCUTILS_LIB_RST,
    get_allowed_uri_schemes,
    get_docutils_settings,
    reload_settings,
    unsafe_docutils_settings_allowed,
)
from django_docutils.lib.writers import DjangoDocutilsWriter
from django_docutils.template import DocutilsTemplate
"""

nitpick_ignore_regex = [
    ("py:.*", r"docutils\..*"),
    ("py:.*", r"django\..*"),
    ("py:.*", r"pygments\..*"),
    ("py:.*", r"typing_extensions\..*"),
    ("py:.*", r"django_docutils\.lib\.transforms\.code\.Token(Stream|Generator)"),
    ("py:class", r"django_docutils\.lib\.roles\.types\.RoleFnReturnValue"),
    ("py:.*", r"nodes\..*"),
    ("py:class", r"Formatter"),
    ("py:class", r"HttpRequest"),
    ("py:class", r"RoleFnReturnValue"),
    ("py:class", r"StrPath"),
    ("py:class", r"frozenset of str"),
    ("py:class", r"mapping"),
    ("py:class", r"optional"),
    ("py:class", r"str or bytes"),
    ("py:class", r"str or None"),
    ("py:obj", r"From:"),
    ("py:obj", r"License:"),
]
