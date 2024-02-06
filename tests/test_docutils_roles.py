# ruff: noqa: E501
"""Tests for docutils roles."""
import typing as t

import pytest
from django.template import Context, Template
from docutils import nodes
from docutils.parsers.rst.states import Inliner

from django_docutils.lib.roles.registry import (
    register_django_docutils_roles,
    register_role_mapping,
)

MAIN_TPL = """
<main>
{content}
</main>

"""


def render_rst_block(contents: str, context: t.Any = None) -> str:
    """Render django template tag {% rst %}{{contents}}{% endrst %}, minus main wrap."""
    if context is None:
        context = {}
    template = Template(
        """{% load django_docutils %}
{% rst %}
{{DEFAULT_RST}}
{% endrst %}
""".replace("{{DEFAULT_RST}}", contents),
    )

    return template.render(Context(context))


class RoleContentFixture(t.NamedTuple):
    """Test docutils role -> django HTML template."""

    # pytest
    test_id: str

    # Assertions
    rst_content: str
    expected_html: str


def test_register_django_docutils_roles(monkeypatch: pytest.MonkeyPatch) -> None:
    """Assertions for register_django_docutils_roles()."""
    from django_docutils.lib.roles import registry as roles_registry_pkg

    assert roles_registry_pkg.DJANGO_DOCUTILS_LIB_RST, (  # type:ignore[attr-defined]
        "Sanity-check, something truthy should be set." ""
    )
    register_django_docutils_roles()

    monkeypatch.setattr(roles_registry_pkg, "DJANGO_DOCUTILS_LIB_RST", {})
    register_django_docutils_roles()

    monkeypatch.setattr(roles_registry_pkg, "DJANGO_DOCUTILS_LIB_RST", {"other": None})
    register_django_docutils_roles()

    monkeypatch.setattr(roles_registry_pkg, "DJANGO_DOCUTILS_LIB_RST", {"roles": {}})
    register_django_docutils_roles()


class SphinxLikeRole:
    """A base class copied from SphinxRole for testing class-based roles.

    This class provides helper methods for Sphinx-like roles.

    .. note:: The subclasses of this class might not work with docutils.
              This class is strongly coupled with Sphinx.
    """

    name: str  #: The role name actually used in the document.
    rawtext: str  #: A string containing the entire interpreted text input.
    text: str  #: The interpreted text content.
    lineno: int  #: The line number where the interpreted text begins.
    inliner: Inliner  #: The ``docutils.parsers.rst.states.Inliner`` object.
    #: A dictionary of directive options for customisation
    #: (from the "role" directive).
    options: dict[str, t.Any]
    #: A list of strings, the directive content for customisation
    #: (from the "role" directive).
    content: t.Sequence[str]

    def __call__(
        self,
        name: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: Inliner,
        options: dict[str, t.Any] | None = None,
        content: t.Sequence[str] = (),
    ) -> tuple[list[nodes.Node], list[t.Any]]:
        """Return example class-based role."""
        self.rawtext = rawtext
        self.text = text
        self.lineno = lineno
        self.inliner = inliner
        self.options = options if options is not None else {}
        self.content = content

        # guess role type
        if name:
            self.name = name.lower()
        return self.run()

    def run(self) -> tuple[list[nodes.Node], list[t.Any]]:
        """Run docutils role."""
        raise NotImplementedError


MySphinxLikeRole = SphinxLikeRole()


def test_register_role_mapping() -> None:
    """Assertions for register_role_mapping()."""
    register_role_mapping({})

    register_role_mapping({"gh": "django_docutils.lib.roles.github.github_role"})

    register_role_mapping(
        {
            "gh": (
                "django_docutils.lib.roles.github.github_role",
                {
                    "lowercase": True,
                    "innernodeclass": "docutils.nodes.inline",
                    "warn_dangling": True,
                },
            ),
        },
    )

    register_role_mapping(
        {
            "ex": (
                "tests.test_docutils_roles.MySphinxLikeRole",
                {
                    "lowercase": True,
                    "innernodeclass": "docutils.nodes.inline",
                    "warn_dangling": True,
                },
            ),
        },
    )

    register_role_mapping(
        {
            "ex": "tests.test_docutils_roles.MySphinxLikeRole",
        },
    )


GH_ROLE_TESTS: list[RoleContentFixture] = [
    RoleContentFixture(
        test_id="gh-role-org",
        rst_content=":gh:`org`\n",
        expected_html='<p><a class="gh reference external offsite" href="https://github.com/org" target="_blank">org</a></p>',
    ),
    RoleContentFixture(
        test_id="gh-role-org",
        rst_content=":gh:`org/repo`\n",
        expected_html='<p><a class="gh reference external offsite" href="https://github.com/org/repo" target="_blank">org/repo</a></p>',
    ),
    RoleContentFixture(
        test_id="gh-role-org",
        rst_content=":gh:`My repo <org/repo>`\n",
        expected_html='<p><a class="gh reference external offsite" href="https://github.com/org/repo" target="_blank">My repo</a></p>',
    ),
    RoleContentFixture(
        test_id="gh-role-org",
        rst_content=":gh:`org/repo#125`\n",
        expected_html='<p><a class="gh reference external offsite" href="https://github.com/org/repo/issue/125" target="_blank">org/repo#125</a></p>',
    ),
    RoleContentFixture(
        test_id="gh-role-org",
        rst_content="My repo :gh:`(#125) <org/repo#125>`\n",
        expected_html='<p>My repo <a class="gh reference external offsite" href="https://github.com/org/repo/issue/125" target="_blank">(#125)</a></p>',
    ),
]


@pytest.mark.parametrize(
    RoleContentFixture._fields,
    GH_ROLE_TESTS,
    ids=[f.test_id for f in GH_ROLE_TESTS],
)
def test_templatetag_gh_role(
    settings: t.Any,
    test_id: str,
    rst_content: str,
    expected_html: str,
) -> None:
    """Asserts gh docutils role."""
    assert render_rst_block(rst_content) == MAIN_TPL.format(content=expected_html)
