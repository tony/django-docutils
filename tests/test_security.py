"""Security posture tests for Docutils rendering."""

from __future__ import annotations

import typing as t

import pytest
from django.template import Context, Template
from docutils import nodes
from docutils.core import publish_doctree as docutils_publish_doctree

from django_docutils.lib.publisher import (
    _uri_is_allowed,
    publish_doctree,
    publish_html_from_doctree,
    publish_html_from_source,
    publish_parts_from_doctree,
    sanitize_doctree,
)
from django_docutils.lib.utils import append_html_to_node
from django_docutils.lib.writers import DjangoDocutilsWriter
from django_docutils.template import DocutilsTemplates
from django_docutils.views import DocutilsView

if t.TYPE_CHECKING:
    import pathlib

    from django.test import RequestFactory


class UnsafeRSTCase(t.NamedTuple):
    """A malicious reStructuredText input and the output it must not emit."""

    test_id: str
    source_template: str
    asset_name: str
    asset_contents: str
    forbidden_html: str


UNSAFE_RST_CASES: list[UnsafeRSTCase] = [
    UnsafeRSTCase(
        test_id="include-file",
        source_template=".. include:: {path}\n",
        asset_name="secret.txt",
        asset_contents="DJANGO-DOCUTILS-SECRET\n",
        forbidden_html="DJANGO-DOCUTILS-SECRET",
    ),
    UnsafeRSTCase(
        test_id="csv-table-file",
        source_template=".. csv-table::\n   :file: {path}\n",
        asset_name="secret.csv",
        asset_contents="DJANGO-DOCUTILS-SECRET\n",
        forbidden_html="DJANGO-DOCUTILS-SECRET",
    ),
    UnsafeRSTCase(
        test_id="raw-file",
        source_template=".. raw:: html\n   :file: {path}\n",
        asset_name="raw.html",
        asset_contents='<script nonce="secret">alert(1)</script>\n',
        forbidden_html="<script",
    ),
    UnsafeRSTCase(
        test_id="raw-html",
        source_template=".. raw:: html\n\n   <script>alert(1)</script>\n",
        asset_name="",
        asset_contents="",
        forbidden_html="<script",
    ),
    UnsafeRSTCase(
        test_id="javascript-link",
        source_template="`click <javascript:alert(1)>`_\n",
        asset_name="",
        asset_contents="",
        forbidden_html='href="javascript:',
    ),
    UnsafeRSTCase(
        test_id="javascript-image",
        source_template=".. image:: javascript:alert(1)\n",
        asset_name="",
        asset_contents="",
        forbidden_html='src="javascript:',
    ),
]


class UnsafeOverrideCase(t.NamedTuple):
    """A trusted opt-in scenario for an unsafe Docutils setting."""

    test_id: str
    docutils_settings: dict[str, object]
    source_template: str
    asset_name: str
    asset_contents: str
    expected_html: str


UNSAFE_OVERRIDE_CASES: list[UnsafeOverrideCase] = [
    UnsafeOverrideCase(
        test_id="raw-html-opt-in",
        docutils_settings={"raw_enabled": True},
        source_template=".. raw:: html\n\n   <script>alert(1)</script>\n",
        asset_name="",
        asset_contents="",
        expected_html="<script",
    ),
    UnsafeOverrideCase(
        test_id="include-file-opt-in",
        docutils_settings={"file_insertion_enabled": True},
        source_template=".. include:: {path}\n",
        asset_name="secret.txt",
        asset_contents="DJANGO-DOCUTILS-SECRET\n",
        expected_html="DJANGO-DOCUTILS-SECRET",
    ),
]


class UnsafeDocutilsConfigCase(t.NamedTuple):
    """A local ``docutils.conf`` attempt to re-enable unsafe rendering."""

    test_id: str
    config_text: str
    source_template: str
    asset_name: str
    asset_contents: str
    forbidden_html: str


UNSAFE_DOCUTILS_CONFIG_CASES: list[UnsafeDocutilsConfigCase] = [
    UnsafeDocutilsConfigCase(
        test_id="raw-enabled-in-docutils-conf",
        config_text="[general]\nraw_enabled: true\n",
        source_template=".. raw:: html\n\n   <script>alert(1)</script>\n",
        asset_name="",
        asset_contents="",
        forbidden_html="<script",
    ),
    UnsafeDocutilsConfigCase(
        test_id="file-insertion-enabled-in-docutils-conf",
        config_text="[general]\nfile_insertion_enabled: true\n",
        source_template=".. include:: {path}\n",
        asset_name="secret.txt",
        asset_contents="DJANGO-DOCUTILS-SECRET\n",
        forbidden_html="DJANGO-DOCUTILS-SECRET",
    ),
]


class DoctreeSanitizerCase(t.NamedTuple):
    """A malicious doctree node created before django-docutils sees it."""

    test_id: str
    source: str
    forbidden_html: str


DOCTREE_SANITIZER_CASES: list[DoctreeSanitizerCase] = [
    DoctreeSanitizerCase(
        test_id="existing-raw-node",
        source=".. raw:: html\n\n   <script>alert(1)</script>\n",
        forbidden_html="<script",
    ),
    DoctreeSanitizerCase(
        test_id="existing-javascript-reference",
        source="`click <javascript:alert(1)>`_\n",
        forbidden_html='href="javascript:',
    ),
    DoctreeSanitizerCase(
        test_id="existing-javascript-image",
        source=".. image:: javascript:alert(1)\n",
        forbidden_html='src="javascript:',
    ),
]


def _render_source(case: UnsafeRSTCase, tmp_path: pathlib.Path) -> str:
    if case.asset_name:
        asset_path = tmp_path / case.asset_name
        asset_path.write_text(case.asset_contents, encoding="utf-8")
        return case.source_template.format(path=asset_path)
    return case.source_template.format(path="")


def _render_override_source(
    case: UnsafeOverrideCase,
    tmp_path: pathlib.Path,
) -> str:
    if case.asset_name:
        asset_path = tmp_path / case.asset_name
        asset_path.write_text(case.asset_contents, encoding="utf-8")
        return case.source_template.format(path=asset_path)
    return case.source_template.format(path="")


def _render_config_source(
    case: UnsafeDocutilsConfigCase,
    tmp_path: pathlib.Path,
) -> str:
    if case.asset_name:
        asset_path = tmp_path / case.asset_name
        asset_path.write_text(case.asset_contents, encoding="utf-8")
        return case.source_template.format(path=asset_path)
    return case.source_template.format(path="")


def _assert_forbidden_html_absent(html: str | None, forbidden_html: str) -> None:
    assert html is not None
    assert forbidden_html not in html


@pytest.mark.parametrize(
    UnsafeRSTCase._fields,
    UNSAFE_RST_CASES,
    ids=[case.test_id for case in UNSAFE_RST_CASES],
)
def test_publish_html_from_source_uses_safe_docutils_defaults(
    tmp_path: pathlib.Path,
    test_id: str,
    source_template: str,
    asset_name: str,
    asset_contents: str,
    forbidden_html: str,
) -> None:
    """Unsafe RST features are disabled by default in source rendering."""
    case = UnsafeRSTCase(
        test_id,
        source_template,
        asset_name,
        asset_contents,
        forbidden_html,
    )
    html = publish_html_from_source(_render_source(case, tmp_path))

    _assert_forbidden_html_absent(html, forbidden_html)


@pytest.mark.parametrize(
    UnsafeRSTCase._fields,
    UNSAFE_RST_CASES,
    ids=[case.test_id for case in UNSAFE_RST_CASES],
)
def test_template_tag_uses_safe_docutils_defaults(
    tmp_path: pathlib.Path,
    test_id: str,
    source_template: str,
    asset_name: str,
    asset_contents: str,
    forbidden_html: str,
) -> None:
    """The public ``{% rst content %}`` tag keeps unsafe RST disabled."""
    case = UnsafeRSTCase(
        test_id,
        source_template,
        asset_name,
        asset_contents,
        forbidden_html,
    )
    template = Template("{% load django_docutils %}{% rst content %}")
    html = template.render(Context({"content": _render_source(case, tmp_path)}))

    assert forbidden_html not in html


@pytest.mark.parametrize(
    UnsafeRSTCase._fields,
    UNSAFE_RST_CASES,
    ids=[case.test_id for case in UNSAFE_RST_CASES],
)
def test_docutils_template_backend_uses_safe_docutils_defaults(
    tmp_path: pathlib.Path,
    test_id: str,
    source_template: str,
    asset_name: str,
    asset_contents: str,
    forbidden_html: str,
) -> None:
    """The Django template backend uses the same locked-down defaults."""
    case = UnsafeRSTCase(
        test_id,
        source_template,
        asset_name,
        asset_contents,
        forbidden_html,
    )
    engine = DocutilsTemplates(
        {
            "NAME": "docutils",
            "DIRS": [],
            "APP_DIRS": False,
            "OPTIONS": {},
        },
    )
    html = engine.from_string(_render_source(case, tmp_path)).render()

    assert forbidden_html not in html


def test_rst_filter_uses_safe_docutils_defaults(tmp_path: pathlib.Path) -> None:
    """The deprecated ``rst`` filter still inherits safe rendering defaults."""
    case = next(case for case in UNSAFE_RST_CASES if case.test_id == "raw-html")
    template = Template("{% load django_docutils %}{{ content|rst }}")

    with pytest.warns(DeprecationWarning):
        html = template.render(Context({"content": _render_source(case, tmp_path)}))

    assert case.forbidden_html not in html


@pytest.mark.parametrize(
    UnsafeDocutilsConfigCase._fields,
    UNSAFE_DOCUTILS_CONFIG_CASES,
    ids=[case.test_id for case in UNSAFE_DOCUTILS_CONFIG_CASES],
)
def test_local_docutils_config_cannot_reenable_unsafe_defaults(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    test_id: str,
    config_text: str,
    source_template: str,
    asset_name: str,
    asset_contents: str,
    forbidden_html: str,
) -> None:
    """Local ``docutils.conf`` files cannot override protected defaults."""
    case = UnsafeDocutilsConfigCase(
        test_id,
        config_text,
        source_template,
        asset_name,
        asset_contents,
        forbidden_html,
    )
    (tmp_path / "docutils.conf").write_text(config_text, encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    html = publish_html_from_source(_render_config_source(case, tmp_path))

    _assert_forbidden_html_absent(html, forbidden_html)


def test_docutils_view_uses_safe_docutils_defaults(
    settings: t.Any,
    tmp_path: pathlib.Path,
    rf: RequestFactory,
) -> None:
    """``DocutilsView`` cannot leak included files through its RST template."""
    request = rf.get("/")
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    settings.TEMPLATES[0].setdefault("DIRS", [str(template_dir)])
    settings.TEMPLATES.append(
        {
            "NAME": "docutils",
            "BACKEND": "django_docutils.template.DocutilsTemplates",
            "DIRS": [str(template_dir)],
            "APP_DIRS": False,
        },
    )
    (template_dir / "base.html").write_text("{{content}}", encoding="utf-8")
    secret_file = tmp_path / "secret.txt"
    secret_file.write_text("DJANGO-DOCUTILS-SECRET\n", encoding="utf-8")
    (template_dir / "home.rst").write_text(
        f".. include:: {secret_file}\n",
        encoding="utf-8",
    )

    class HomeView(DocutilsView):
        template_name = "base.html"
        rst_name = "home.rst"

    home_view = HomeView()
    home_view.setup(request)
    response = home_view.render_to_response()
    response.render()  # type:ignore[attr-defined]

    assert "DJANGO-DOCUTILS-SECRET" not in response.content.decode("utf-8")


@pytest.mark.parametrize(
    DoctreeSanitizerCase._fields,
    DOCTREE_SANITIZER_CASES,
    ids=[case.test_id for case in DOCTREE_SANITIZER_CASES],
)
def test_publish_html_from_doctree_sanitizes_existing_unsafe_nodes(
    test_id: str,
    source: str,
    forbidden_html: str,
) -> None:
    """HTML publishing sanitizes unsafe nodes in caller-supplied doctrees."""
    doctree = docutils_publish_doctree(
        source,
        settings_overrides={
            "file_insertion_enabled": True,
            "raw_enabled": True,
        },
    )

    html = publish_html_from_doctree(doctree)

    _assert_forbidden_html_absent(html, forbidden_html)


@pytest.mark.parametrize(
    DoctreeSanitizerCase._fields,
    DOCTREE_SANITIZER_CASES,
    ids=[case.test_id for case in DOCTREE_SANITIZER_CASES],
)
def test_publish_parts_from_doctree_sanitizes_existing_unsafe_nodes(
    test_id: str,
    source: str,
    forbidden_html: str,
) -> None:
    """Part publishing sanitizes unsafe nodes in caller-supplied doctrees."""
    doctree = docutils_publish_doctree(
        source,
        settings_overrides={
            "file_insertion_enabled": True,
            "raw_enabled": True,
        },
    )

    parts = publish_parts_from_doctree(doctree, writer=DjangoDocutilsWriter())

    assert forbidden_html not in parts["html_body"]


@pytest.mark.parametrize(
    UnsafeOverrideCase._fields,
    UNSAFE_OVERRIDE_CASES,
    ids=[case.test_id for case in UNSAFE_OVERRIDE_CASES],
)
def test_unsafe_docutils_settings_require_explicit_project_opt_in(
    settings: t.Any,
    tmp_path: pathlib.Path,
    test_id: str,
    docutils_settings: dict[str, object],
    source_template: str,
    asset_name: str,
    asset_contents: str,
    expected_html: str,
) -> None:
    """Dangerous settings remain disabled without the unsafe opt-in flag."""
    case = UnsafeOverrideCase(
        test_id,
        docutils_settings,
        source_template,
        asset_name,
        asset_contents,
        expected_html,
    )
    settings.DJANGO_DOCUTILS_LIB_RST = {
        "docutils": docutils_settings,
    }

    html = publish_html_from_source(_render_override_source(case, tmp_path))

    _assert_forbidden_html_absent(html, expected_html)


@pytest.mark.parametrize(
    UnsafeOverrideCase._fields,
    UNSAFE_OVERRIDE_CASES,
    ids=[case.test_id for case in UNSAFE_OVERRIDE_CASES],
)
def test_unsafe_docutils_settings_can_be_enabled_for_trusted_rst(
    settings: t.Any,
    tmp_path: pathlib.Path,
    test_id: str,
    docutils_settings: dict[str, object],
    source_template: str,
    asset_name: str,
    asset_contents: str,
    expected_html: str,
) -> None:
    """Trusted static RST can opt back into specific unsafe Docutils settings."""
    case = UnsafeOverrideCase(
        test_id,
        docutils_settings,
        source_template,
        asset_name,
        asset_contents,
        expected_html,
    )
    settings.DJANGO_DOCUTILS_LIB_RST = {
        "allow_unsafe_docutils_settings": True,
        "docutils": docutils_settings,
    }

    html = publish_html_from_source(_render_override_source(case, tmp_path))

    assert html is not None
    assert expected_html in html


class UriAllowCase(t.NamedTuple):
    """A URI and whether the scheme allow-list may emit it."""

    test_id: str
    uri: str
    allowed: bool


URI_ALLOW_CASES: list[UriAllowCase] = [
    UriAllowCase(
        test_id="plain-https",
        uri="https://example.com",
        allowed=True,
    ),
    UriAllowCase(
        test_id="relative",
        uri="/path/page",
        allowed=True,
    ),
    UriAllowCase(
        test_id="fragment",
        uri="#section",
        allowed=True,
    ),
    UriAllowCase(
        test_id="javascript",
        uri="javascript:alert(1)",
        allowed=False,
    ),
    UriAllowCase(
        test_id="uppercase-scheme",
        uri="JAVASCRIPT:alert(1)",
        allowed=False,
    ),
    UriAllowCase(
        test_id="leading-space",
        uri="  javascript:alert(1)",
        allowed=False,
    ),
    UriAllowCase(
        test_id="embedded-tab",
        uri="java\tscript:alert(1)",
        allowed=False,
    ),
    UriAllowCase(
        test_id="embedded-newline",
        uri="java\nscript:alert(1)",
        allowed=False,
    ),
    UriAllowCase(
        test_id="embedded-cr",
        uri="java\rscript:alert(1)",
        allowed=False,
    ),
    UriAllowCase(
        test_id="vertical-tab",
        uri="java\x0bscript:alert(1)",
        allowed=False,
    ),
    UriAllowCase(
        test_id="c0-control",
        uri="java\x01script:alert(1)",
        allowed=False,
    ),
    UriAllowCase(
        test_id="invalid-ipv6",
        uri="http://[::1",
        allowed=False,
    ),
]


@pytest.mark.parametrize(
    UriAllowCase._fields,
    URI_ALLOW_CASES,
    ids=[case.test_id for case in URI_ALLOW_CASES],
)
def test_uri_is_allowed_rejects_obfuscated_schemes(
    test_id: str,
    uri: str,
    allowed: bool,
) -> None:
    """Scheme obfuscation must not slip past the URI allow-list."""
    assert _uri_is_allowed(uri, frozenset({"https"})) is allowed


class TrustedMarkupCase(t.NamedTuple):
    """Library-generated markup that must survive locked-down rendering."""

    test_id: str
    source: str
    expected_html: str
    forbidden_html: str | None


TRUSTED_MARKUP_CASES: list[TrustedMarkupCase] = [
    TrustedMarkupCase(
        test_id="kbd-role",
        source=":kbd:`ctrl-t`",
        expected_html="<kbd>ctrl-t</kbd>",
        forbidden_html=None,
    ),
    TrustedMarkupCase(
        test_id="kbd-role-comma",
        source=":kbd:`ctrl-t,shift`",
        expected_html="<kbd>ctrl-t</kbd><kbd>shift</kbd>",
        forbidden_html=None,
    ),
    TrustedMarkupCase(
        test_id="kbd-role-ampersand",
        source=":kbd:`A&B`",
        expected_html="<kbd>A&amp;B</kbd>",
        forbidden_html="<kbd>A&B</kbd>",
    ),
    TrustedMarkupCase(
        test_id="kbd-role-angle-brackets",
        source=":kbd:`<Enter>`",
        expected_html="<kbd>&lt;Enter&gt;</kbd>",
        forbidden_html="<kbd><Enter></kbd>",
    ),
    TrustedMarkupCase(
        test_id="kbd-role-script-breakout",
        source=":kbd:`</kbd><script>alert(1)</script><kbd>`",
        expected_html=(
            "<kbd>&lt;/kbd&gt;&lt;script&gt;alert(1)&lt;/script&gt;&lt;kbd&gt;</kbd>"
        ),
        forbidden_html="<script>alert(1)</script>",
    ),
]


@pytest.mark.parametrize(
    TrustedMarkupCase._fields,
    TRUSTED_MARKUP_CASES,
    ids=[case.test_id for case in TRUSTED_MARKUP_CASES],
)
def test_library_markup_survives_locked_down_rendering(
    test_id: str,
    source: str,
    expected_html: str,
    forbidden_html: str | None,
) -> None:
    """django-docutils' own markup renders safely under safe defaults."""
    html = publish_html_from_source(source)

    assert html is not None
    assert expected_html in html
    if forbidden_html is not None:
        assert forbidden_html not in html


class KbdDoctreeCase(t.NamedTuple):
    """A kbd role source and the key labels it should preserve as text nodes."""

    test_id: str
    source: str
    expected_texts: tuple[str, ...]


KBD_DOCTREE_CASES: list[KbdDoctreeCase] = [
    KbdDoctreeCase(
        test_id="kbd-role-inline-node",
        source=":kbd:`ctrl-t`",
        expected_texts=("ctrl-t",),
    ),
    KbdDoctreeCase(
        test_id="kbd-role-comma-inline-nodes",
        source=":kbd:`ctrl-t,shift`",
        expected_texts=("ctrl-t", "shift"),
    ),
]


@pytest.mark.parametrize(
    KbdDoctreeCase._fields,
    KBD_DOCTREE_CASES,
    ids=[case.test_id for case in KBD_DOCTREE_CASES],
)
def test_kbd_role_uses_escaped_doctree_nodes(
    test_id: str,
    source: str,
    expected_texts: tuple[str, ...],
) -> None:
    """The kbd role must not trust user-controlled labels as raw HTML."""
    doctree = publish_doctree(source)

    assert not list(doctree.findall(nodes.raw))
    kbd_nodes = [
        node
        for node in doctree.findall(nodes.inline)
        if "kbd" in node.get("classes", [])
    ]
    assert tuple(node.astext() for node in kbd_nodes) == expected_texts


def test_inline_code_survives_doctree_re_render() -> None:
    """Re-rendering a doctree keeps CodeTransform's highlighted inline code.

    CodeTransform replaces literals with raw nodes in place during the first
    publish; sanitization on a second publish of the same doctree must not
    delete them.
    """
    doctree = publish_doctree("Run ``$ ls -la`` now.")

    first = publish_html_from_doctree(doctree)
    second = publish_html_from_doctree(doctree)

    assert first is not None
    assert second is not None
    for html in (first, second):
        assert "inline-code" in html
        assert "ls" in html


class SanitizeMisuseCase(t.NamedTuple):
    """A direct sanitize_doctree call with caller-supplied raw settings."""

    test_id: str
    rst_settings: dict[str, object]
    expect_raw_kept: bool


SANITIZE_MISUSE_CASES: list[SanitizeMisuseCase] = [
    SanitizeMisuseCase(
        test_id="raw-enabled-without-opt-in",
        rst_settings={"docutils": {}},
        expect_raw_kept=False,
    ),
    SanitizeMisuseCase(
        test_id="raw-enabled-with-opt-in",
        rst_settings={"allow_unsafe_docutils_settings": True},
        expect_raw_kept=True,
    ),
]


@pytest.mark.parametrize(
    SanitizeMisuseCase._fields,
    SANITIZE_MISUSE_CASES,
    ids=[case.test_id for case in SANITIZE_MISUSE_CASES],
)
def test_sanitize_doctree_raw_skip_requires_project_opt_in(
    settings: t.Any,
    test_id: str,
    rst_settings: dict[str, object],
    expect_raw_kept: bool,
) -> None:
    """Caller-supplied raw_enabled cannot bypass stripping without the opt-in."""
    settings.DJANGO_DOCUTILS_LIB_RST = rst_settings
    document = nodes.document("", "")  # type: ignore[arg-type]
    document += nodes.raw("", "<script></script>", format="html")

    sanitize_doctree(document, {"raw_enabled": True})

    assert bool(list(document.findall(nodes.raw))) is expect_raw_kept


def test_malformed_link_does_not_fail_render() -> None:
    """RST with an unparsable link URI renders instead of raising."""
    html = publish_html_from_source("`x <http://[::1>`_")

    assert html is not None
    assert "http://[::1" not in html


def test_append_html_to_node_survives_sanitization() -> None:
    """HTML injected via append_html_to_node persists under safe defaults."""
    doctree = publish_doctree("content\n")
    paragraph = next(iter(doctree.findall(nodes.paragraph)))
    append_html_to_node(paragraph, "<span>injected</span>")

    sanitize_doctree(doctree)

    raw_nodes = list(doctree.findall(nodes.raw))
    assert any("injected" in raw_node.astext() for raw_node in raw_nodes)
