"""Tests for user-facing documentation examples."""

from __future__ import annotations

import pathlib
import re
import typing as t

import pytest
from django.template import Context, Template

from django_docutils.views import DocutilsResponse, DocutilsView

if t.TYPE_CHECKING:
    from django.test import RequestFactory


_REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
_DOCS_ROOT = _REPO_ROOT / "docs"
_FENCE_RE = re.compile(
    r"^(?P<fence>`{3,}|~{3,})(?P<language>[^\n]*)\n"
    r"(?P<body>.*?)"
    r"^(?P=fence)\s*$",
    re.MULTILINE | re.DOTALL,
)


class TemplateSnippetCase(t.NamedTuple):
    """A documented Django template example and its rendered HTML block."""

    test_id: str
    path: pathlib.Path
    snippet_contains: str
    expects_deprecation: bool


class PageContractCase(t.NamedTuple):
    """A prose-level documentation contract."""

    test_id: str
    path: pathlib.Path
    required: tuple[str, ...]
    forbidden: tuple[str, ...]


TEMPLATE_SNIPPET_CASES: list[TemplateSnippetCase] = [
    TemplateSnippetCase(
        test_id="template-tag",
        path=_DOCS_ROOT / "topics" / "template_tag.md",
        snippet_contains="{% rst %}",
        expects_deprecation=False,
    ),
    TemplateSnippetCase(
        test_id="template-filter",
        path=_DOCS_ROOT / "topics" / "template_filter.md",
        snippet_contains="{% filter rst %}",
        expects_deprecation=True,
    ),
    TemplateSnippetCase(
        test_id="quickstart-first-block",
        path=_DOCS_ROOT / "quickstart.md",
        snippet_contains="{% rst %}",
        expects_deprecation=False,
    ),
]

PAGE_CONTRACT_CASES: list[PageContractCase] = [
    PageContractCase(
        test_id="quickstart-renders-first-snippet",
        path=_DOCS_ROOT / "quickstart.md",
        required=("{% rst %}", "Output:"),
        forbidden=("pipx", "uvx"),
    ),
    PageContractCase(
        test_id="template-filter-is-legacy",
        path=_DOCS_ROOT / "topics" / "template_filter.md",
        required=("deprecated", "{ref}`template_tag`"),
        forbidden=(),
    ),
]


def _read_docs_page(path: pathlib.Path) -> str:
    """Return a docs source page."""
    return path.read_text(encoding="utf-8")


def _fenced_blocks(path: pathlib.Path, language: str) -> list[str]:
    """Return fenced code blocks for ``language`` from a docs source page."""
    return [
        match.group("body").rstrip("\n")
        for match in _FENCE_RE.finditer(_read_docs_page(path))
        if match.group("language").strip() == language
    ]


def _first_fenced_block(path: pathlib.Path, language: str) -> str:
    """Return the first fenced block for ``language`` from ``path``."""
    blocks = _fenced_blocks(path, language)
    assert blocks, f"{path} has no {language!r} fenced block"
    return blocks[0]


def _fenced_block_containing(path: pathlib.Path, language: str, needle: str) -> str:
    """Return the first fenced block for ``language`` that contains ``needle``."""
    for block in _fenced_blocks(path, language):
        if needle in block:
            return block
    msg = f"{path} has no {language!r} fenced block containing {needle!r}"
    raise AssertionError(msg)


def _normalize_html(value: str) -> str:
    """Normalize rendered HTML for docs example comparisons."""
    return value.strip()


@pytest.mark.parametrize(
    TemplateSnippetCase._fields,
    TEMPLATE_SNIPPET_CASES,
    ids=[case.test_id for case in TEMPLATE_SNIPPET_CASES],
)
def test_template_topic_examples_render_documented_html(
    test_id: str,
    path: pathlib.Path,
    snippet_contains: str,
    expects_deprecation: bool,
    settings: t.Any,
) -> None:
    """Template topic examples must render the HTML documented beside them."""
    source = _fenced_block_containing(path, "django", snippet_contains)
    expected_html = _first_fenced_block(path, "html")

    if expects_deprecation:
        with pytest.warns(DeprecationWarning):
            rendered = Template(source).render(Context())
    else:
        rendered = Template(source).render(Context())

    assert _normalize_html(rendered) == expected_html


def test_class_based_view_example_renders_documented_html(
    settings: t.Any,
    tmp_path: pathlib.Path,
    rf: RequestFactory,
) -> None:
    """The class-based view topic's RST example must render its shown output."""
    path = _DOCS_ROOT / "topics" / "class_based_view.md"
    rst_source = _first_fenced_block(path, "restructuredtext")
    base_template = _first_fenced_block(path, "django")
    expected_html = _first_fenced_block(path, "html")
    request = rf.get("/")
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    settings.TEMPLATES[0].setdefault("DIRS", [str(template_dir)])
    settings.TEMPLATES.append(
        {
            "NAME": "docutils",
            "BACKEND": "django_docutils.template.DocutilsTemplates",
            "DIRS": [str(template_dir)],
            "APP_DIRS": True,
        },
    )
    (template_dir / "base.html").write_text(base_template, encoding="utf-8")
    (template_dir / "home.rst").write_text(rst_source, encoding="utf-8")

    class HomeView(DocutilsView):
        template_name = "base.html"
        rst_name = "home.rst"

    home_view = HomeView()
    home_view.setup(request)
    response = t.cast(DocutilsResponse, home_view.render_to_response())
    response.render()

    assert _normalize_html(response.content.decode("utf-8")) == expected_html


@pytest.mark.parametrize(
    PageContractCase._fields,
    PAGE_CONTRACT_CASES,
    ids=[case.test_id for case in PAGE_CONTRACT_CASES],
)
def test_docs_pages_follow_dx_contracts(
    test_id: str,
    path: pathlib.Path,
    required: tuple[str, ...],
    forbidden: tuple[str, ...],
) -> None:
    """High-traffic pages must keep reader-facing DX promises."""
    source = _read_docs_page(path)

    for text in required:
        assert text in source
    for text in forbidden:
        assert text not in source
