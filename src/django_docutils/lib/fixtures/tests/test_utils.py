import pathlib

import pytest
from django.apps import apps

from django_docutils.lib.fixtures.tests.conftest import create_bare_app
from django_docutils.lib.fixtures.utils import (
    find_app_configs_with_fixtures,
    find_rst_files,
    find_rst_files_in_app,
    get_model_from_post_app,
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


def test_find_app_configs_with_fixtures(sample_app_config):
    assert sample_app_config in find_app_configs_with_fixtures(has_rst_files=False)


def test_find_app_configs_with_fixtures_with_rst_files(bare_app_config):
    assert bare_app_config not in find_app_configs_with_fixtures()
    assert bare_app_config not in find_app_configs_with_fixtures(has_rst_files=False)
    assert bare_app_config not in find_app_configs_with_fixtures(has_rst_files=True)


def test_find_app_configs_with_fixtures_with_empty_fixtures_dir(
    bare_app_config_with_empty_fixture_dir,
):
    assert bare_app_config_with_empty_fixture_dir in find_app_configs_with_fixtures(
        has_rst_files=False
    )
    assert bare_app_config_with_empty_fixture_dir not in find_app_configs_with_fixtures(
        has_rst_files=True
    )


def test_find_rst_files_in_app(sample_app_config):
    assert "./hi.rst" in find_rst_files_in_app(sample_app_config)
    assert "2017/06/04/moo.rst" not in find_rst_files_in_app(sample_app_config)


def test_get_model_from_post_app():
    app = apps.get_app_config("test_app")
    assert get_model_from_post_app(app) == app.get_model("RSTPost")
