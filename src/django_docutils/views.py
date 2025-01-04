"""Django-docutils class-based view for django (and its' parts)."""

from __future__ import annotations

import typing as t

from django.core.exceptions import ImproperlyConfigured
from django.template.loader import select_template
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

if t.TYPE_CHECKING:
    from django.http.request import HttpRequest
    from django.http.response import HttpResponse


class DocutilsResponse(TemplateResponse):
    """Docutils TemplateResponse."""

    template_name = "base.html"

    def __init__(
        self,
        request: HttpRequest,
        template: list[str],
        rst: list[str],
        context: dict[str, t.Any] | None = None,
        content_type: str | None = None,
        status: int | None = None,
        charset: str | None = None,
        using: str | None = None,
    ) -> None:
        self.rst_name = rst
        super().__init__(
            request,
            template,
            context,
            content_type,
            status,
            charset,
            using,
        )

    @property
    def rendered_content(self) -> str:
        """Return freshly rendered content via docutils engine."""
        context: dict[str, t.Any] = self.resolve_context(self.context_data) or {}

        # we should be able to use the engine to .Render this
        from django.utils.safestring import mark_safe

        context["content"] = mark_safe(
            select_template(self.rst_name, using="docutils").render(),
        )

        template = self.resolve_template(self.template_name)
        return template.render(context)  # type:ignore


class DocutilsViewRstNameImproperlyConfigured(ImproperlyConfigured):
    """DocutilsView could not find rst_name."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        return super().__init__(
            "DocutilsView requires either a definition of 'rst_name' or an "
            "implementation of 'get_rst_names()'",
            *args,
            **kwargs,
        )


class DocutilsView(TemplateView):
    """Django-docutils view, renders reStructuredText to HTML via rst_name."""

    response_class = DocutilsResponse
    rst_name: str | None = None

    def render_to_response(
        self,
        context: dict[str, t.Any] | None = None,
        content_type: str | None = None,
        status: int | None = None,
        charset: str | None = None,
        using: str | None = None,
        **response_kwargs: object,
    ) -> HttpResponse:
        """Override to pay in rst content."""
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            rst=self.get_rst_names(),
            context=context,
            content_type=content_type,
            status=status,
            using=using or self.template_engine,
        )

    def get_rst_names(self) -> list[str]:
        """Follows after get_template_names, but for scanning for rst content."""
        if self.rst_name is None:
            raise DocutilsViewRstNameImproperlyConfigured
        return [self.rst_name]
