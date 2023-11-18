"""Tests for DocutilsView template view."""
import pathlib
import typing as t

from django_docutils.views import DocutilsView

from .constants import DEFAULT_RST

if t.TYPE_CHECKING:
    from django.test import RequestFactory


def test_view(settings: t.Any, tmp_path: pathlib.Path, rf: "RequestFactory") -> None:
    """Assert DocutilsView renders HTML from reStructuredText."""
    request = rf.get("/")
    template_dir = tmp_path / "templates"
    if not template_dir.exists():
        template_dir.mkdir()
    settings.TEMPLATES[0].setdefault("DIRS", [str(template_dir)])
    settings.TEMPLATES.append(
        {
            "NAME": "docutils",
            "BACKEND": "django_docutils.template.DocutilsTemplates",
            "DIRS": [str(template_dir)],
            "APP_DIRS": True,
        }
    )
    base_html = template_dir / "base.html"
    base_html.write_text("{{content}}", encoding="utf-8")

    home_rst = template_dir / "home.rst"
    home_rst.write_text(
        DEFAULT_RST,
        encoding="utf-8",
    )

    class HomeView(DocutilsView):
        template_name = "base.html"
        rst_name = "home.rst"

    home_view = HomeView()
    home_view.setup(request)
    rendered_response = home_view.render_to_response()
    rendered_response.render()  # type:ignore
    assert (
        rendered_response.content.decode("utf-8")
        == r"""<div class="document" id="hey">
<h1 class="title">hey</h1>
<h2 class="subtitle" id="hi">hi</h2>
<ol class="upperalpha simple">
<li>hows</li>
<li>it</li>
<li>going</li>
<li>today</li>
</ol>
<p><strong>hi</strong>
<em>hi</em></p>
</div>

"""
    )
