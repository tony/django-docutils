from django.apps import apps

from django_docutils.lib.fixtures.utils import (
    find_app_configs_with_fixtures,
    find_rst_files,
    find_rst_files_in_app,
    get_model_from_post_app,
)


def test_find_rst_files(tmpdir):
    tmpdir.join('hi.rst').write('')
    tmpdir.join('not_at_rst_file.html').write('')
    tmpdir.mkdir('wat')
    tmpdir.join('wat/moo.rst').write('')
    tmpdir.join('wat/another.rst').write('')

    assert ['./hi.rst'] == find_rst_files(str(tmpdir))


def test_find_app_configs_with_fixtures(sample_app_config):
    assert sample_app_config in find_app_configs_with_fixtures()


def test_find_rst_files_in_app(sample_app_config):
    assert './hi.rst' in find_rst_files_in_app(sample_app_config)
    assert '2017/06/04/moo.rst' not in find_rst_files_in_app(sample_app_config)


def test_get_model_from_post_app():
    app = apps.get_app_config('test_app')
    assert get_model_from_post_app(app) == app.get_model('RSTPost')
