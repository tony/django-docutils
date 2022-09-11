"""Test reST fixture files in directory format, "dir"."""

from django_docutils.lib.fixtures.directory.utils import find_rst_dir_projects


def test_find_rst_dir_projects(tmpdir):
    tmpdir.mkdir("wat")
    tmpdir.join("wat/README.rst").write("")
    tmpdir.join("wat/manifest.json").write("")

    assert [str(tmpdir.join("wat"))] == find_rst_dir_projects(str(tmpdir))
