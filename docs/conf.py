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
    extra_extensions=["sphinx_click.ext"],
    intersphinx_mapping={
        "python": ("http://docs.python.org/", None),
        "django": (
            "https://docs.djangoproject.com/en/4.2/",
            "https://docs.djangoproject.com/en/4.2/_objects/",
        ),
    },
    linkcode_resolve=make_linkcode_resolve(django_docutils, about["__github__"]),
    html_favicon="_static/favicon.ico",
    html_extra_path=["manifest.json"],
    rediraffe_redirects="redirects.txt",
    autodoc_mock_imports=["django"],
    set_type_checking_flag=True,
)
globals().update(conf)
