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
        return publish_html_from_doctree(
            self.doctree, **getattr(self, "rst_settings", {})
        )

    def get_base_template(self):
        """TODO: move this out of RSTMixin, it is AMP related, not RST"""
        if self.request.GET.get("is_amp", False):
            return "based/base-amp.html"
        else:
            return "base.html"


class RSTRawView(TemplateTitleView):

    """Send pure reStructuredText to template.

    Requires template tags to process it.

    .. code-block:: html

       {% block content %}
         <div id="content_wrapper" class="content docutils-html fixed-toc-content">
           {% restructuredtext content show_title=False inject_ads=False %}
         </div>
       {% endblock content %}

       {% block sidebar %}
         {% restructuredtext content toc_only=True %}
       {% endblock sidebar %}

    """

    template_name = "rst/raw.html"
    file_path = None
    title = None
    rst_settings = {"inject_ads": True}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = open(self.file_path, "r").read()
        context["inject_ads"] = self.rst_settings["inject_ads"]
        return context


class RSTView(RSTRawView, RSTMixin):
    template_name = "rst/base.html"
    file_path = None
    title = None
    rst_settings = {"inject_ads": True}

    @cached_property
    def raw_content(self):
        return open(self.file_path, "r").read()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = self.content
        context["sidebar"] = self.sidebar

        return context
