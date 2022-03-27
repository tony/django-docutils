import py
import pytest

from django_docutils.lib.fixtures.tests.conftest import create_bare_app


@pytest.fixture()
def sample_dir_app_config(tmpdir_factory, request, settings):
    """Return a Django AppConfig for a project with a directory-style
    fixture inside of it.

    It will automatically remove from INSTALLED_APPS and clean created
    files on teardown. See :func:`create_bare_app`.

    :rtype: :class:`django.apps.apps.AppConfig`
    :returns: a bare app config with temporary file structure created
    """
    conf = """{
  "Programming_languages": ["python"],
  "Topics": ["Web Frameworks"],
  "Slug_Id": "Te5t17fr",
  "Created": "2017-09-12",
  "Author": "tony"
}
""".strip()

    content = """=============================================
Learn JavaScript for free: The best resources
=============================================

first section
-------------

some content
""".strip()

    tmpdir = tmpdir_factory.mktemp("sample_dir_project")

    sample_app = create_bare_app(
        project_tmpdir=tmpdir,
        request=request,
        settings=settings,
        app_name="sample_dir_app",
    )

    sample_app_dir = py.path.local(sample_app.path)

    sample_app_dir.join("__init__.py").write("")

    # give it a fixtures dir
    fixtures_dir = sample_app_dir.ensure("fixtures", dir=True)
    fixtures_dir.join("hi.rst").write("")
    fixtures_dir.ensure("sample_project", dir=True)
    fixtures_dir.join("sample_project").join("manifest.json").write(conf)
    fixtures_dir.join("sample_project").join("README.rst").write(content)

    return sample_app


@pytest.fixture()
def sample_dir_series_app_config(tmpdir_factory, request, settings):
    """Returns a "multi-file" directory-style fixture.

    :rtype: :class:`django.apps.apps.AppConfig`
    :returns: a bare app config with temporary file structure created
    """

    conf = """{
  "Programming_languages": ["python"],
  "Topics": ["Web Frameworks"],
  "Slug_Id": "Te3y28vm",
  "Created": "2017-10-20",
  "Author": "tony",
  "Series": [
    "README.rst",
    "page2.rst",
    "page3.rst"
  ]
}
""".strip()

    content = """=============
A test series
=============
hi there
--------

first section
-------------

some content
""".strip()

    content2 = """=============
A test series
=============
page 2
------

first section of page 2
-----------------------

some content for page 2
""".strip()

    content3 = """=============
A test series
=============
page 3
------

first section of page 3
-----------------------

some content for page 3
""".strip()

    BASE_FOLDER = "sample_dir_series_project1"

    tmpdir = tmpdir_factory.mktemp(BASE_FOLDER)

    sample_app = create_bare_app(tmpdir, request, settings, "sample_dir_series_app")

    sample_app_dir = py.path.local(sample_app.path)

    sample_app_dir.join("__init__.py").write("")

    # give it a fixtures dir
    fixtures_dir = sample_app_dir.ensure("fixtures", dir=True)

    # the app's fixtures/ dir
    fixtures_dir.join("hi.rst").write("")
    fixtures_dir.mkdir(BASE_FOLDER)

    # The RST project inside the app's fixtures dir
    project_dir = fixtures_dir.join(BASE_FOLDER)
    project_dir.join("manifest.json").write(conf)
    project_dir.join("README.rst").write(content)
    project_dir.join("page2.rst").write(content2)
    project_dir.join("page3.rst").write(content3)

    return sample_app
