import pathlib

import pytest
from django.apps import AppConfig

from django_docutils.lib.fixtures.load import load_app_rst_fixtures


@pytest.mark.django_db(transaction=True)
def test_load_app_rst_fixtures_bare(bare_app_config, RSTPost):
    """Verifies the fixture acts as expected."""
    assert isinstance(bare_app_config, AppConfig)

    bare_app = pathlib.Path(bare_app_config.path)
    fixtures_dir = bare_app / "fixtures"
    if not fixtures_dir.exists():
        fixtures_dir.mkdir()
    test_file = fixtures_dir / "test.rst"
    test_file.write_text(
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
