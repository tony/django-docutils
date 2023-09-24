import typing as t

from django.core.exceptions import ImproperlyConfigured
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.template.loader import select_template
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

if t.TYPE_CHECKING:
    from typing_extensions import TypedDict, Unpack


class DocutilsResponse(TemplateResponse):
    template_name = "base.html"

    def __init__(
        self,
        request: HttpRequest,
        template: list[str],
        rst: list[str],
        context: t.Optional[t.Dict[str, t.Any]] = None,
        content_type: t.Optional[str] = None,
        status: t.Optional[int] = None,
        charset: t.Optional[str] = None,
        using: t.Optional[str] = None,
    ):
        self.rst_name = rst
        super().__init__(
            request, template, context, content_type, status, charset, using
        )

    @property
    def rendered_content(self) -> str:
        """Return the freshly rendered content for the template and context
        described by the TemplateResponse.

        This *does not* set the final content of the response. To set the
        response content, you must either call render(), or set the
        content explicitly using the value of this property.
        """

        context: t.Dict[str, t.Any] = self.resolve_context(self.context_data) or {}

        # we should be able to use the engine to .Render this
        from django.utils.safestring import mark_safe

        context["content"] = mark_safe(
            select_template(self.rst_name, using="docutils").render()
        )

        template = self.resolve_template(self.template_name)
        content = template.render(context)
        return content


class DocutilsViewRstNameImproperlyConfigured(ImproperlyConfigured):
    def __init__(self, *args: object, **kwargs: object) -> None:
        return super().__init__(
            "DocutilsView requires either a definition of 'rst_name' "
            "or an implementation of 'get_rst_names()'",
            *args,
            **kwargs
        )


class DocutilsView(TemplateView):
    response_class = DocutilsResponse
    rst_name = None

    def render_to_response(
        self,
        context: t.Optional[t.Dict[str, t.Any]] = None,
        content_type: t.Optional[str] = None,
        status: t.Optional[int] = None,
        charset: t.Optional[str] = None,
        using: t.Optional[str] = None,
        **response_kwargs: object
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
        """
        Follows after get_template_names, but for scanning for rst content.
        """
        if self.rst_name is None:
            raise DocutilsViewRstNameImproperlyConfigured()
        else:
            return [self.rst_name]
