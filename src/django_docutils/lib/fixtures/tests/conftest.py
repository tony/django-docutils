import pathlib
import shutil
import sys

import pytest
from django.apps import apps

from django_docutils.favicon.tests.conftest import RSTPost, favicon_app  # NOQA


def create_bare_app(project_tmp_path, request, settings, app_name):
    """Create a blank django project for PyTest that cleans out of scope.

    Intended for use inside of PyTest Fixtures.

    :param project_tmp_path: root of the django project

       This cleans up automatically after the fixture falls out of scope.
    :type project_tmp_path: :class:`pathlib.Path`
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

    bare_app = project_tmp_path / app_name
    if not bare_app.exists():
        bare_app.mkdir()

    (bare_app / "__init__.py").write_text("")

    if str(project_tmp_path) not in sys.path:
        sys.path.append(str(project_tmp_path))
    settings.INSTALLED_APPS = (*settings.INSTALLED_APPS, app_name)

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
def bare_app_config(tmp_path_factory: pytest.TempPathFactory, request, settings):
    """Return a Django AppConfig for a blank project.

    It will automatically remove from INSTALLED_APPS and clean created
    files on teardown. See :func:`create_bare_app`.

    :rtype: :class:`django.apps.apps.AppConfig`
    :returns: a bare app config with temporary file structure created
    """

    tmp_path = tmp_path_factory.mktemp("bare_project")

    return create_bare_app(tmp_path, request, settings, "bare_app")


@pytest.fixture(scope="function")
def sample_app_config(tmp_path_factory: pytest.TempPathFactory, request, settings):
    tmp_path = tmp_path_factory.mktemp("sample_project")

    sample_app = create_bare_app(tmp_path, request, settings, "sample_app")

    sample_app_dir = pathlib.Path(sample_app.path)

    # give it a fixtures dir
    fixtures_dir = sample_app_dir / "fixtures"

    if not fixtures_dir.exists():
        fixtures_dir.mkdir(parents=True)

    (fixtures_dir / "hi.rst").write_text(
        """
===
moo
===

:Author: anonymous
:Slug_Id: tEst

foo
    """.strip()
    )
    deep_dir = fixtures_dir / "2017" / "06" / "04"
    if not deep_dir.exists():
        deep_dir.mkdir(parents=True)
    (deep_dir / "moo.rst").write_text("h")

    return sample_app
