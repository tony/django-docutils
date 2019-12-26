# flake8: NOQA: F401

import pytest

from django.apps import apps


@pytest.fixture
def EmptyModel(favicon_app):
    return favicon_app.get_model('EmptyModel')


@pytest.fixture
def Favicon(favicon_app):
    return favicon_app.get_model('Favicon')


@pytest.fixture
def RSTPost(favicon_app):
    return favicon_app.get_model('RSTPost')


@pytest.fixture
def RSTPostPage(favicon_app):
    return favicon_app.get_model('RSTPostPage')


@pytest.fixture
def favicon_app(settings, request):
    app_name = 'test_app'
    app_import_string = f'django_docutils.favicon.tests.{app_name}'

    if app_import_string not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS = settings.INSTALLED_APPS + (app_import_string,)

    def resource_a_teardown():
        print('\nresources_a_teardown()')
        settings.INSTALLED_APPS = (
            s for s in settings.INSTALLED_APPS if s != app_import_string
        )

        assert app_import_string not in settings.INSTALLED_APPS

    request.addfinalizer(resource_a_teardown)

    return apps.get_app_config(app_name)
