import shutil
import sys

import py
import pytest

import factory
from django.apps import apps
from django.contrib.auth import get_user_model
from pytest_factoryboy import register

from django_docutils.favicon.tests.conftest import RSTPost, favicon_app  # NOQA


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: "user%03d" % n)
    password = factory.Sequence(lambda n: "pass%03d" % n)


register(UserFactory)


def create_bare_app(project_tmpdir, request, settings, app_name):
    """Create a blank django project for PyTest that cleans out of scope.

    Intended for use inside of PyTest Fixtures.

    :param project_tmpdir: root of the django project

       This cleans up automatically after the fixture falls out of scope.
    :type project_tmpdir: :class:`py._path.local.LocalPath`
    :param request: PyTest request object (dependency injected)
    :type request: :class:`pytest.fixtures.FixtureRequest`
    :param settings: django settings fixture (from pytest-django)

        From pytest-django docs:

        "This fixture will provide a handle on the Django settings module, and
         automatically revert any changes made to the settings (modifications,
         additions and deletions).
    :type settings: :class:`pytest_django.fixtures.settings`
    :param app_name: application name
    :type app_name: str
    :rtype: :class:`django.apps.apps.AppConfig`
    :returns: a bare app config with temporary file structure created
    """

    bare_app = project_tmpdir.mkdir(app_name)

    bare_app.join("__init__.py").write("")

    if project_tmpdir.strpath not in sys.path:
        sys.path.append(project_tmpdir.strpath)
    settings.INSTALLED_APPS = settings.INSTALLED_APPS + (app_name,)

    def resource_a_teardown():
        print("\nresources_a_teardown()")
        # todo replace 'bare_app' with app_name
        settings.INSTALLED_APPS = (
            s for s in settings.INSTALLED_APPS if s != "bare_app"
        )

        assert app_name not in settings.INSTALLED_APPS
        shutil.rmtree(str(bare_app))

    request.addfinalizer(resource_a_teardown)

    return apps.get_app_config(app_name)


@pytest.fixture(scope="function")
def bare_app_config(tmpdir_factory, request, settings):
    """Return a Django AppConfig for a blank project.

    It will automatically remove from INSTALLED_APPS and clean created
    files on teardown. See :func:`create_bare_app`.

    :rtype: :class:`django.apps.apps.AppConfig`
    :returns: a bare app config with temporary file structure created
    """

    tmpdir = tmpdir_factory.mktemp("bare_project")

    return create_bare_app(tmpdir, request, settings, "bare_app")


@pytest.fixture(scope="function")
def sample_app_config(tmpdir_factory, request, settings):
    tmpdir = tmpdir_factory.mktemp("sample_project")

    sample_app = create_bare_app(tmpdir, request, settings, "sample_app")

    sample_app_dir = py.path.local(sample_app.path)

    # give it a fixtures dir
    fixtures_dir = sample_app_dir.ensure("fixtures", dir=True)

    fixtures_dir.join("hi.rst").write(
        """
===
moo
===

:Author: anonymous
:Slug_Id: tEst

foo
    """.strip()
    )
    fixtures_dir.ensure("2017", dir=True)
    fixtures_dir.join("2017").ensure("06", dir=True)
    fixtures_dir.join("2017").join("06").ensure("04", dir=True)
    fixtures_dir.join("2017").join("06").join("04").join("moo.rst").write("h")

    return sample_app
