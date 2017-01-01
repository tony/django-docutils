# -*- coding: utf-8 -*-

import django

from django.core.exceptions import ImproperlyConfigured

from django.views.generic.base import TemplateView
from django.template.response import TemplateResponse
from django.template.loader import select_template

class DocutilsResponse(TemplateResponse):

    template_name = 'base.html'

    def __init__(self, request, template, rst, context=None, content_type=None,
            status=None, charset=None, using=None):
        self.rst_name = rst
        super(DocutilsResponse, self).__init__(
            request, template, context, content_type, status, charset, using)

    @property
    def rendered_content(self):
        """Return the freshly rendered content for the template and context
        described by the TemplateResponse.

        This *does not* set the final content of the response. To set the
        response content, you must either call render(), or set the
        content explicitly using the value of this property.
        """


        if django.VERSION < (1, 10):
            context = self._resolve_context(self.context_data)
        else:
            context = self.resolve_context(self.context_data)

        # we should be able to use the engine to .Render this
        from django.utils.safestring import mark_safe
        context['content'] = mark_safe(select_template(self.rst_name, using='docutils').render())

        if django.VERSION < (1, 10):
            template = self._resolve_template(self.template_name)
        else:
            template = self.resolve_template(self.template_name)
        content = template.render(context, self._request)
        return content


class DocutilsView(TemplateView):
    response_class = DocutilsResponse
    rst_name = None

    def render_to_response(self, context, **response_kwargs):
        """Override to pay in rst content."""
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            rst=self.get_rst_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_rst_names(self):
        """
        Follows after get_template_names, but for scanning for rst content.
        """
        if self.rst_name is None:
            raise ImproperlyConfigured(
                "DocutilsView requires either a definition of "
                "'rst_name' or an implementation of 'get_rst_names()'")
        else:
            return [self.rst_name]
