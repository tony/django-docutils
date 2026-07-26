#!/usr/bin/env python3
"""Runtime dependency smoke test for django-docutils.

Imports every module in the ``django_docutils`` package and renders a small
reStructuredText document through the public API. It is meant to run inside an
environment that has *only* the package's runtime dependencies installed, so
that a dependency which is declared under ``[dependency-groups]`` (or merely
pulled in transitively by a dev tool) but imported at runtime is caught before
release. ``typing_extensions`` is the motivating example.

Run it against a clean build::

    uvx --isolated --no-cache --from . python scripts/runtime_dep_smoketest.py
"""

from __future__ import annotations

import argparse
import importlib
import pkgutil
import sys
import typing as t

ModuleName = str

DEFAULT_PACKAGE = "django_docutils"

SMOKE_TEST_RST = """\
Heading
=======

Hello **world**, see :pypi:`django-docutils`.

Sub one
-------

Text.

Sub two
-------

.. code-block:: python

   print("hi")
"""
"""Exercises the writer, a role, the code directive, and the TOC transform.

Two sub-sections are required for the TOC transform to emit anything.
"""


def parse_args(argv: t.Sequence[str] | None = None) -> argparse.Namespace:
    """Return parsed CLI arguments for the smoke test runner.

    Parameters
    ----------
    argv : sequence of str, optional
        Argument vector; defaults to ``sys.argv[1:]``.

    Returns
    -------
    argparse.Namespace
        Parsed arguments.

    Examples
    --------
    >>> parse_args(["--skip-render"]).skip_render
    True
    >>> parse_args([]).package
    'django_docutils'
    """
    parser = argparse.ArgumentParser(
        description=(
            "Probe django-docutils' runtime dependencies by importing every "
            "module and rendering reStructuredText through the public API."
        ),
    )
    parser.add_argument(
        "--package",
        default=DEFAULT_PACKAGE,
        help=f"Root package to inspect (defaults to {DEFAULT_PACKAGE}).",
    )
    parser.add_argument(
        "--skip-imports",
        action="store_true",
        help="Skip module import validation.",
    )
    parser.add_argument(
        "--skip-render",
        action="store_true",
        help="Skip the reStructuredText render check.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print each module as it is imported.",
    )
    return parser.parse_args(argv)


def configure_django() -> None:
    """Bootstrap Django the way a project depending on django-docutils would.

    django-docutils reads ``DJANGO_DOCUTILS_LIB_RST`` at import time, so the
    settings object must exist before any module is imported.

    Roles and directives register only from ``DJANGO_DOCUTILS_LIB_RST``, and
    docutils degrades an unregistered role or directive into an error node
    instead of raising. Bootstrapping without them would leave the render check
    exercising neither pygments nor the role machinery, while still passing.

    Examples
    --------
    >>> configure_django()
    >>> from django.conf import settings
    >>> settings.configured
    True
    """
    import django
    from django.conf import settings

    if settings.configured:
        return

    settings.configure(
        INSTALLED_APPS=["django_docutils"],
        TEMPLATES=[{"BACKEND": "django_docutils.template.DocutilsTemplates"}],
        DJANGO_DOCUTILS_LIB_RST={
            "directives": {
                "code-block": "django_docutils.lib.directives.code.CodeBlock",
            },
            "roles": {
                "local": {"pypi": "django_docutils.lib.roles.pypi.pypi_role"},
            },
        },
    )
    django.setup()


def discover_modules(package_name: str) -> list[ModuleName]:
    """Return a sorted list of module names within *package_name*.

    Parameters
    ----------
    package_name : str
        Importable root package.

    Returns
    -------
    list of str
        Every module in the package, including the package itself.

    Examples
    --------
    >>> discover_modules("argparse")
    ['argparse']
    >>> "django_docutils.lib.publisher" in discover_modules("django_docutils")
    True
    """
    package = importlib.import_module(package_name)
    module_names: set[str] = {package_name}
    package_path = getattr(package, "__path__", None)
    if package_path is None:
        return sorted(module_names)
    module_names.update(
        module_info.name
        for module_info in pkgutil.walk_packages(
            package_path,
            prefix=f"{package_name}.",
        )
    )
    return sorted(module_names)


def import_all_modules(module_names: list[ModuleName], verbose: bool) -> list[str]:
    """Import each module, returning a failure message per module that raised.

    Parameters
    ----------
    module_names : list of str
        Modules to import.
    verbose : bool
        Echo each module name to stdout as it is imported.

    Returns
    -------
    list of str
        Failure messages; empty when every module imported.

    Examples
    --------
    >>> import_all_modules(["argparse"], verbose=False)
    []
    >>> import_all_modules(["django_docutils.no_such_module"], verbose=False)
    ['django_docutils.no_such_module: ModuleNotFoundError(...)']
    """
    failures: list[str] = []
    for module_name in module_names:
        if verbose:
            sys.stdout.write(f"import {module_name}\n")
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            failures.append(f"{module_name}: {exc!r}")
    return failures


def exercise_api(verbose: bool) -> list[str]:
    """Render reStructuredText through the public API, returning failures.

    Importing a module only proves its *top-level* imports resolve. A
    dependency imported lazily inside a function body — or a docutils
    component registered on first use — stays invisible until something is
    actually rendered, so exercise the public entry points here.

    Parameters
    ----------
    verbose : bool
        Echo each check to stdout as it runs.

    Returns
    -------
    list of str
        Failure messages; empty when every check passed.

    Examples
    --------
    >>> configure_django()
    >>> exercise_api(verbose=False)
    []
    """
    from django_docutils.lib.publisher import (
        publish_doctree,
        publish_html_from_source,
        publish_toc_from_doctree,
    )

    failures: list[str] = []

    if verbose:
        sys.stdout.write("render publish_html_from_source\n")
    try:
        html = publish_html_from_source(SMOKE_TEST_RST) or ""
    except Exception as exc:
        failures.append(f"publish_html_from_source: {exc!r}")
    else:
        # docutils renders an unregistered role or directive as an error node
        # rather than raising, so assert on the markers each dependency leaves
        # behind. Without them a missing dependency renders a broken document
        # and still exits 0.
        if "system-message" in html.lower():
            failures.append("publish_html_from_source: docutils emitted an error node")
        if "highlight" not in html:
            failures.append("publish_html_from_source: pygments did not highlight")
        if "pypi.python.org" not in html:
            failures.append("publish_html_from_source: pypi role did not resolve")

    if verbose:
        sys.stdout.write("render publish_toc_from_doctree\n")
    try:
        toc = publish_toc_from_doctree(publish_doctree(SMOKE_TEST_RST))
    except Exception as exc:
        failures.append(f"publish_toc_from_doctree: {exc!r}")
    else:
        if not toc:
            failures.append("publish_toc_from_doctree: returned no table of contents")

    return failures


def main(argv: t.Sequence[str] | None = None) -> int:
    """Entry point for the runtime dependency smoke test.

    Parameters
    ----------
    argv : sequence of str, optional
        Argument vector; defaults to ``sys.argv[1:]``.

    Returns
    -------
    int
        ``0`` when every check passed, ``1`` otherwise.

    Examples
    --------
    >>> main(["--package", "argparse", "--skip-render"])
    0
    """
    args = parse_args(argv)
    failures: list[str] = []

    configure_django()

    if not args.skip_imports:
        try:
            modules = discover_modules(args.package)
        except Exception as exc:
            failures.append(f"{args.package}: {exc!r}")
        else:
            failures.extend(import_all_modules(modules, args.verbose))

    if not args.skip_render:
        failures.extend(exercise_api(args.verbose))

    if failures:
        for failure in failures:
            sys.stderr.write(f"{failure}\n")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
