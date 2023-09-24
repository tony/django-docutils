import typing as t

from django.conf import settings
from django.http.request import HttpRequest
from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
from django.template.engine import Engine
from django.template.exceptions import TemplateDoesNotExist
from docutils import core

from .directives import register_pygments_directive


class Docutils(BaseEngine):
    app_dirname = "templates"

    def __init__(self, params: t.Dict[str, t.Any]) -> None:
        params = params.copy()
        self.options = params.pop("OPTIONS").copy()
        self.options.setdefault("debug", settings.DEBUG)
        super().__init__(params)
        self.engine = Engine(self.dirs, self.app_dirs, **self.options)

    def from_string(self, template_code: str) -> "DocutilsTemplate":
        return DocutilsTemplate(template_code, self.options)

    def get_template(self, template_name: str) -> "DocutilsTemplate":
        for template_file in self.iter_template_filenames(template_name):
            try:
                with open(template_file, encoding="utf-8") as fp:
                    template_code = fp.read()
            except OSError:
                continue

            return DocutilsTemplate(template_code, self.options)
        else:
            raise TemplateDoesNotExist(template_name)


class DocutilsTemplate:
    def __init__(self, source: str, options: t.Dict[str, t.Any]) -> None:
        self.source = source
        self.options = options

    def render(
        self,
        context: t.Optional[t.Dict[str, t.Any]] = None,
        request: t.Optional[HttpRequest] = None,
    ) -> str:
        context = self.options
        if request is not None:
            context["request"] = request
            context["csrf_input"] = csrf_input_lazy(request)
            context["csrf_token"] = csrf_token_lazy(request)
        context = {"source": self.source, "writer_name": "html"}

        return t.cast(str, core.publish_parts(**context)["html_body"])


register_pygments_directive()
