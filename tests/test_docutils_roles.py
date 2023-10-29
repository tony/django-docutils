"""Tests for docutils roles."""
import typing as t

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


def test_templatetag_gh_role(settings: t.Any) -> None:
    """Asserts gh docutils role."""
    assert render_rst_block(":gh:`org`\n") == MAIN_TPL.format(
        content='<p><a class="gh reference external offsite" href="https://github.com/org" target="_blank">org</a></p>'  # noqa: E501
    )

    assert render_rst_block(":gh:`org/repo`\n") == MAIN_TPL.format(
        content='<p><a class="gh reference external offsite" href="https://github.com/org/repo" target="_blank">org/repo</a></p>'  # noqa: E501
    )

    assert render_rst_block(":gh:`My repo <org/repo>`\n") == MAIN_TPL.format(
        content='<p><a class="gh reference external offsite" href="https://github.com/org/repo" target="_blank">My repo</a></p>'  # noqa: E501
    )

    assert render_rst_block(":gh:`org/repo#125`\n") == MAIN_TPL.format(
        content='<p><a class="gh reference external offsite" href="https://github.com/org/repo/issue/125" target="_blank">org/repo#125</a></p>'  # noqa: E501
    )

    assert render_rst_block("My repo :gh:`(#125) <org/repo#125>`\n") == MAIN_TPL.format(
        content='<p>My repo <a class="gh reference external offsite" href="https://github.com/org/repo/issue/125" target="_blank">(#125)</a></p>'  # noqa: E501
    )
