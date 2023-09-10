import pathlib

from django.utils.functional import cached_property
from django.views.generic.base import ContextMixin, TemplateView

from django_docutils.lib.publisher import (
    publish_doctree,
    publish_html_from_doctree,
    publish_toc_from_doctree,
)

from .text import smart_title


class TitleMixin(ContextMixin):
    title = None
    subtitle = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title:
            context["title"] = smart_title(self.title)
        if self.subtitle:
            context["subtitle"] = smart_title(self.subtitle)
        return context


class TemplateTitleView(TemplateView, TitleMixin):
    title = None
    subtitle = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RSTMixin:
    @cached_property
    def raw_content(self):
        raise NotImplementedError

    @cached_property
    def doctree(self):
        return publish_doctree(self.raw_content)

    @cached_property
    def sidebar(self, **kwargs):
        return publish_toc_from_doctree(self.doctree)

    @cached_property
    def content(self):
        return publish_html_from_doctree()

    def get_base_template(self):
        """TODO: move this out of RSTMixin, it is AMP related, not RST"""
        if self.request.GET.get("is_amp", False):
            return "django_docutils/base-amp.html"
        else:
            return "base.html"


class RSTRawView(TemplateTitleView):

    """Send pure reStructuredText to template.

    Requires template tags to process it.

    .. code-block:: html

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
    file_path = None
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with pathlib.Path(self.file_path).open() as content:
            context["content"] = content.read()
        return context


class RSTView(RSTRawView, RSTMixin):
    template_name = "rst/base.html"
    file_path = None
    title = None

    @cached_property
    def raw_content(self):
        with pathlib.Path(self.file_path).open() as raw_content:
            return raw_content

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = self.content
        context["sidebar"] = self.sidebar

        return context
