"""Django view machinery for rendering docutils content as HTML."""
import pathlib
import typing as t

from django.http import HttpRequest
from django.utils.functional import cached_property
from django.views.generic.base import ContextMixin, TemplateView
from docutils import nodes

from .._internal.types import StrPath
from .publisher import (
    publish_doctree,
    publish_html_from_doctree,
    publish_toc_from_doctree,
)
from .text import smart_title


class TitleMixin(ContextMixin):
    """ContextMixin that capitalizes title and subtitle."""

    title = None
    subtitle = None

    def get_context_data(self, **kwargs: object) -> t.Dict[str, t.Any]:
        """:func:`django_docutils.lib.text.smart_title()` on title and subtitle."""
        context = super().get_context_data(**kwargs)
        if self.title:
            context["title"] = smart_title(self.title)
        if self.subtitle:
            context["subtitle"] = smart_title(self.subtitle)
        return context


class TemplateTitleView(TemplateView, TitleMixin):
    """Combination of Template and Title mixin."""

    title = None
    subtitle = None

    def get_context_data(self, **kwargs: object) -> t.Dict[str, t.Any]:
        """Return context data."""
        return super().get_context_data(**kwargs)


class RSTMixin:
    """Django Class-based view mixin for reStructuredText."""

    request: HttpRequest

    @cached_property
    def raw_content(self) -> t.Optional[str]:
        """Raw reStructuredText content."""
        raise NotImplementedError

    @cached_property
    def doctree(self) -> nodes.document | None:
        """Return docutils doctree of RST content (pre-HTML)."""
        if self.raw_content is None:
            return None

        return publish_doctree(self.raw_content)

    @cached_property
    def sidebar(self, **kwargs: object) -> str | None:
        """Return table of contents sidebar of RST content as HTML."""
        if self.doctree is None:
            return None

        return publish_toc_from_doctree(self.doctree)

    @cached_property
    def content(self) -> str | None:
        """Return reStructuredText content as HTML."""
        if self.doctree is None:
            return None

        return publish_html_from_doctree(
            self.doctree,
            **getattr(self, "rst_settings", {}),
        )

    def get_base_template(self) -> str:
        """TODO: move this out of RSTMixin, it is AMP related, not RST."""
        if self.request.GET.get("is_amp", False):
            return "django_docutils/base-amp.html"
        else:
            return "base.html"


class RSTRawView(TemplateTitleView):
    """Send pure reStructuredText to template.

    Requires template tags to process it.

    .. code-block:: django

       {% load django_docutils %}
       {% block content %}
         <div id="content_wrapper" class="content docutils-html fixed-toc-content">
           {% restructuredtext content show_title=False %}
         </div>
       {% endblock content %}

       {% block sidebar %}
         {% restructuredtext content toc_only=True %}
       {% endblock sidebar %}

    """

    template_name = "rst/raw.html"
    file_path: t.Optional[StrPath] = None
    title = None

    def get_context_data(self, **kwargs: object) -> t.Dict[str, t.Any]:
        """Merge content to context data."""
        context = super().get_context_data(**kwargs)

        if self.file_path is not None:
            with pathlib.Path(self.file_path).open() as content:
                context["content"] = content.read()

        return context


class RSTView(RSTRawView, RSTMixin):
    """RestructuredText Django View."""

    template_name = "rst/base.html"
    file_path: t.Optional[StrPath] = None
    title = None

    @cached_property
    def raw_content(self) -> t.Optional[str]:
        """Raw reStructuredText data."""
        if self.file_path is None:
            return None

        with pathlib.Path(self.file_path).open() as raw_content:
            return raw_content.read()

    def get_context_data(self, **kwargs: object) -> t.Dict[str, t.Any]:
        """Merge content and sidebar to context data."""
        context = super().get_context_data(**kwargs)
        context["content"] = self.content
        context["sidebar"] = self.sidebar

        return context
