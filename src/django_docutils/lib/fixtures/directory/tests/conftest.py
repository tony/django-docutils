import pathlib

import pytest

from django_docutils.lib.fixtures.tests.conftest import create_bare_app


@pytest.fixture()
def sample_dir_app_config(tmp_path_factory, request, settings):
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

    tmp_path = tmp_path_factory.mktemp("sample_dir_project")

    sample_app = create_bare_app(
        project_tmp_path=tmp_path,
        request=request,
        settings=settings,
        app_name="sample_dir_app",
    )

    sample_app_dir = pathlib.Path(sample_app.path)

    (sample_app_dir / "__init__.py").write_text("")

    # give it a fixtures dir
    fixtures_dir = sample_app_dir / "fixtures"

    if not fixtures_dir.exists():
        fixtures_dir.mkdir()
    (fixtures_dir / "hi.rst").write_text("")

    sample_project = fixtures_dir / "sample_project"
    if not sample_project.exists():
        sample_project.mkdir()

    (sample_project / "manifest.json").write_text(conf)
    (sample_project / "README.rst").write_text(content)

    return sample_app


@pytest.fixture()
def sample_dir_series_app_config(tmp_path_factory, request, settings):
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

    tmp_path = tmp_path_factory.mktemp(BASE_FOLDER)

    sample_app = create_bare_app(tmp_path, request, settings, "sample_dir_series_app")

    sample_app_dir = pathlib.Path(sample_app.path)

    (sample_app_dir / "__init__.py").write_text("")

    # give it a fixtures dir
    fixtures_dir = sample_app_dir / "fixtures"
    if not fixtures_dir.exists():
        fixtures_dir.mkdir()

    # the app's fixtures/ dir
    (fixtures_dir / "hi.rst").write_text("")
    base_folder = fixtures_dir / BASE_FOLDER

    if not base_folder.exists():
        base_folder.mkdir()

    # The RST project inside the app's fixtures dir
    (base_folder / "manifest.json").write_text(conf)
    (base_folder / "README.rst").write_text(content)
    (base_folder / "page2.rst").write_text(content2)
    (base_folder / "page3.rst").write_text(content3)

    return sample_app
