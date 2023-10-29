"""Tests for docutils roles."""
import typing as t

import pytest
from django.template import Context, Template

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
""".replace("{{DEFAULT_RST}}", contents)
    )

    return template.render(Context(context))


class RoleContentFixture(t.NamedTuple):
    """Test docutils role -> django HTML template."""

    # pytest
    test_id: str

    # Assertions
    rst_content: str
    expected_html: str


GH_ROLE_TESTS: list[RoleContentFixture] = [
    RoleContentFixture(
        test_id="gh-role-org",
        rst_content=":gh:`org`\n",
        expected_html='<p><a class="gh reference external offsite" href="https://github.com/org" target="_blank">org</a></p>',  # noqa: E501
    ),
    RoleContentFixture(
        test_id="gh-role-org",
        rst_content=":gh:`org/repo`\n",
        expected_html='<p><a class="gh reference external offsite" href="https://github.com/org/repo" target="_blank">org/repo</a></p>',  # noqa: E501
    ),
    RoleContentFixture(
        test_id="gh-role-org",
        rst_content=":gh:`My repo <org/repo>`\n",
        expected_html='<p><a class="gh reference external offsite" href="https://github.com/org/repo" target="_blank">My repo</a></p>',  # noqa: E501
    ),
    RoleContentFixture(
        test_id="gh-role-org",
        rst_content=":gh:`org/repo#125`\n",
        expected_html='<p><a class="gh reference external offsite" href="https://github.com/org/repo/issue/125" target="_blank">org/repo#125</a></p>',  # noqa: E501
    ),
    RoleContentFixture(
        test_id="gh-role-org",
        rst_content="My repo :gh:`(#125) <org/repo#125>`\n",
        expected_html='<p>My repo <a class="gh reference external offsite" href="https://github.com/org/repo/issue/125" target="_blank">(#125)</a></p>',  # noqa: E501
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
