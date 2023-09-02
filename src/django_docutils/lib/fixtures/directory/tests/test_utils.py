"""Test reST fixture files in directory format, "dir"."""

from django_docutils.lib.fixtures.directory.utils import find_rst_dir_projects


def test_find_rst_dir_projects(tmp_path):
    other_dir = tmp_path / "other_dir"

    if not other_dir.exists():
        other_dir.mkdir()

    (other_dir / "README.rst").write_text("")
    (other_dir / "manifest.json").write_text("")

    assert [str(other_dir)] == find_rst_dir_projects(str(tmp_path))
