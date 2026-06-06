"""Django template engine for Docutils."""

from __future__ import annotations

import typing as t

from django.conf import settings
from django.http.request import HttpRequest
from django.template import Context
from django.template.backends.base import BaseEngine
from django.template.engine import Engine
from django.template.exceptions import TemplateDoesNotExist
from django.utils.safestring import SafeString, mark_safe
from docutils import writers

from django_docutils.lib.directives.code import register_pygments_directive
from django_docutils.lib.publisher import publish_doctree, publish_parts_from_doctree


class DocutilsTemplates(BaseEngine):
    """Docutils engine for Django."""

    app_dirname: str = "templates"

    def __init__(self, params: dict[str, t.Any]) -> None:
        params = params.copy()
        self.options = params.pop("OPTIONS").copy()
        self.options.setdefault("debug", settings.DEBUG)
        super().__init__(params)
        self.engine = Engine(self.dirs, self.app_dirs, **self.options)

    def from_string(self, template_code: str) -> DocutilsTemplate:
        """Return DocutilsTemplate from string."""
        return DocutilsTemplate(template_code, self.options)

    def get_template(self, template_name: str) -> DocutilsTemplate:
        """Return template from template_name."""
        for template_file in self.iter_template_filenames(template_name):
            try:
                with open(template_file, encoding="utf-8") as fp:
                    template_code = fp.read()
            except OSError:
                continue

            return DocutilsTemplate(template_code, self.options)
        raise TemplateDoesNotExist(template_name)


class DocutilsTemplate:
    """Docutils template object for Django. Used by Docutils template engine."""

    def __init__(self, source: str, options: dict[str, t.Any]) -> None:
        self.source = source
        self.options = options

    def render(
        self,
        context: Context | dict[str, t.Any] | None = None,
        request: HttpRequest | None = None,
    ) -> SafeString:
        """Render DocutilsTemplate to string."""
        writer = writers.get_writer_class("html")()
        doctree = publish_doctree(self.source)
        parts = publish_parts_from_doctree(doctree, writer=writer)["html_body"]
        assert isinstance(parts, str)

        return mark_safe(parts)


register_pygments_directive()
