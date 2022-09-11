import pytest

from django_docutils.exc import BasedException
from django_docutils.lib.fixtures.directory.extract import extract_dir_config
from django_docutils.lib.fixtures.directory.utils import (
    find_rst_dirs_in_app,
    find_series_files,
)


def test_dir_with_series(sample_dir_series_app_config):
    project_paths = find_rst_dirs_in_app(sample_dir_series_app_config)

    assert len(project_paths) == 1

    project_path = project_paths[0]  # pick out the project

    config = extract_dir_config(project_path)

    # this function automatically checks that series files exist
    find_series_files(config, project_path)

    # raises exception if files not found
    with pytest.raises(BasedException, match=r"Files in .*"):
        # test it with missing files
        missing_file_config = config.copy()
        missing_file_config["series"].append("non-existant-file.rst")
        find_series_files(missing_file_config, project_path)
