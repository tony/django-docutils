"""Django template engine for Docutils."""
import typing as t

from django.conf import settings
from django.http.request import HttpRequest
from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
from django.template.engine import Engine
from django.template.exceptions import TemplateDoesNotExist
from django.utils.safestring import mark_safe
from docutils import core

from django_docutils.lib.directives.code import register_pygments_directive

if t.TYPE_CHECKING:
    from django.template.backends.base import _EngineTemplate
    from django.template.base import Context
    from django.utils.safestring import SafeString


class DocutilsTemplates(BaseEngine):
    """Docutils engine for Django."""

    app_dirname: str = "templates"

    def __init__(self, params: t.Dict[str, t.Any]) -> None:
        params = params.copy()
        self.options = params.pop("OPTIONS").copy()
        self.options.setdefault("debug", settings.DEBUG)
        super().__init__(params)
        self.engine = Engine(self.dirs, self.app_dirs, **self.options)

    def from_string(self, template_code: str) -> "DocutilsTemplate":
        """Return DocutilsTemplate from string."""
        return DocutilsTemplate(template_code, self.options)

    def get_template(self, template_name: str) -> "_EngineTemplate":
        """Return template from template_name."""
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
    """Docutils template object for Django. Used by Docutils template engine."""

    def __init__(self, source: str, options: t.Dict[str, t.Any]) -> None:
        self.source = source
        self.options = options

    def render(
        self,
        context: t.Union["Context", t.Dict[str, t.Any], None] = None,
        request: t.Optional[HttpRequest] = None,
    ) -> "SafeString":
        """Render DocutilsTemplate to string."""
        context = self.options
        if request is not None:
            context["request"] = request
            context["csrf_input"] = csrf_input_lazy(request)
            context["csrf_token"] = csrf_token_lazy(request)
        context = {"source": self.source, "writer_name": "html"}

        return mark_safe(t.cast(str, core.publish_parts(**context)["html_body"]))


register_pygments_directive()
