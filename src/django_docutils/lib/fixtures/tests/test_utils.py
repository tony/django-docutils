import pathlib

import pytest

from django_docutils.lib.fixtures.tests.conftest import create_bare_app
from django_docutils.lib.fixtures.utils import (
    find_rst_files,
)


@pytest.fixture(scope="function")
def bare_app_config_with_empty_fixture_dir(tmp_path_factory, request, settings):
    tmp_path = tmp_path_factory.mktemp("bare_project")

    app_config = create_bare_app(tmp_path, request, settings, "app_with_empty_fixtures")
    sample_app_dir = pathlib.Path(app_config.path)
    fixtures_dir = sample_app_dir / "fixtures"

    if not fixtures_dir.exists():
        fixtures_dir.mkdir()
    yield app_config


def test_find_rst_files(tmp_path):
    (tmp_path / "hi.rst").write_text("")
    (tmp_path / "not_at_rst_file.html").write_text("")

    other_dir = tmp_path / "other_dir"
    if not other_dir.exists():
        other_dir.mkdir()

    (other_dir / "moo.rst").write_text("")
    (other_dir / "another.rst").write_text("")

    assert ["./hi.rst"] == find_rst_files(str(tmp_path))
