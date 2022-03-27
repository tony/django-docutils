import py
import pytest

from django.apps import AppConfig

from django_docutils.lib.fixtures.load import load_app_rst_fixtures


@pytest.mark.django_db(transaction=True)
def test_load_app_rst_fixtures_bare(bare_app_config, RSTPost):
    """Verifies the fixture acts as expected."""
    assert isinstance(bare_app_config, AppConfig)

    bare_app = py.path.local(bare_app_config.path)
    fixtures_dir = bare_app.ensure("fixtures", dir=True)
    test_file = fixtures_dir.join("test.rst")
    test_file.write(
        """
===
moo
===

:Author: anonymous
:Slug_Id: tEst

foo
    """.strip()
    )

    posts = load_app_rst_fixtures(bare_app_config, model=RSTPost)
    assert len(posts) == 1
