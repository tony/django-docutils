# -*- coding: utf-8 -*-

import io

from django.conf import settings
try:
    from django.template.base import TemplateDoesNotExist
except ImportError: # >= 1.9
    from django.template.exceptions import TemplateDoesNotExist
from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
from django.template.engine import Engine

from docutils import core

from .directives import register_pygments_directive


class Docutils(BaseEngine):
    app_dirname = 'templates'

    def __init__(self, params):
        params = params.copy()
        self.options = params.pop('OPTIONS').copy()
        self.options.setdefault('debug', settings.DEBUG)
        self.options.setdefault('file_charset', settings.FILE_CHARSET)
        super(Docutils, self).__init__(params)
        self.engine = Engine(self.dirs, self.app_dirs, **self.options)

    def from_string(self, template_code):
        return DocutilsTemplate(template_code, self.options)

    def get_template(self, template_name):
        for template_file in self.iter_template_filenames(template_name):
            try:
                with io.open(template_file, encoding=settings.FILE_CHARSET) as fp:
                    template_code = fp.read()
            except IOError:
                continue

            return DocutilsTemplate(template_code, self.options)
        else:
            raise TemplateDoesNotExist(template_name)


class DocutilsTemplate(object):

    def __init__(self, source, options):
        self.source = source
        self.options = options

    def render(self, context=None, request=None):
        context = self.options
        if request is not None:
            context['request'] = request
            context['csrf_input'] = csrf_input_lazy(request)
            context['csrf_token'] = csrf_token_lazy(request)
        context = {
            'source': self.source,
            'writer_name': 'html'
        }

        return core.publish_parts(**context)['html_body']


register_pygments_directive()
