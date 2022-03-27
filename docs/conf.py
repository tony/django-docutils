# -*- coding: utf-8 -*-
# flake8: noqa E501
import os
import sys
from pathlib import Path

# Get the project root dir, which is the parent dir of this
cwd = Path.cwd()
project_root = cwd.parent

sys.path.insert(0, str(project_root))
sys.path.insert(0, str(cwd / "_ext"))


# package data
about = {}
with open("../django_docutils/__about__.py") as fp:
    exec(fp.read(), about)

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_issues",
    "sphinx_click.ext",  # sphinx-click
    "sphinx_inline_tabs",
    "sphinx_copybutton",
    "sphinxext.opengraph",
    "sphinxext.rediraffe",
    "myst_parser",
]
myst_enable_extensions = ["colon_fence", "substitution", "replacements"]

issues_github_path = about["__github__"].replace("https://github.com/", "")

templates_path = ["_templates"]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

master_doc = "index"

project = about["__title__"]
copyright = about["__copyright__"]

version = "%s" % (".".join(about["__version__"].split("."))[:2])
release = "%s" % (about["__version__"])

exclude_patterns = ["_build"]

pygments_style = "monokai"
pygments_dark_style = "monokai"

html_favicon = "_static/favicon.ico"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_extra_path = ["manifest.json"]
html_theme = "furo"
html_theme_options = {}

html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/projects.html",
        "sidebar/scroll-end.html",
    ]
}

# sphinxext.opengraph
ogp_site_url = about["__docs__"]
ogp_image = "_static/img/icons/icon-192x192.png"
ogp_desscription_length = about["__description__"]
ogp_site_name = about["__title__"]

# sphinx-copybutton
copybutton_prompt_text = (
    r">>> |\.\.\. |> |\$ |\# | In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
)
copybutton_prompt_is_regexp = True
copybutton_remove_prompts = True

# sphinxext-rediraffe
rediraffe_redirects = "redirects.txt"
rediraffe_branch = "master~1"


htmlhelp_basename = "%sdoc" % about["__title__"]

latex_documents = [
    (
        "index",
        "{0}.tex".format(about["__package_name__"]),
        "{0} Documentation".format(about["__title__"]),
        about["__author__"],
        "manual",
    ),
]

man_pages = [
    (
        "index",
        about["__package_name__"],
        "{0} Documentation".format(about["__title__"]),
        about["__author__"],
        1,
    ),
]

texinfo_documents = [
    (
        "index",
        "{0}".format(about["__package_name__"]),
        "{0} Documentation".format(about["__title__"]),
        about["__author__"],
        about["__package_name__"],
        about["__description__"],
        "Miscellaneous",
    ),
]

intersphinx_mapping = {
    "python": ("http://docs.python.org/", None),
}
