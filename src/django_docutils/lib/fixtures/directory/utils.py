"""
This format is different:

1. It resides in its own directory
2. Includes a JSON file
3. Does not store configuration in the RST file itself

This is intended to ensure these projects can be open source repositories
with collaborators on GitHub.

Here is what a layout of "dir"-type RST fixtures look like:

fixtures/
- myproject/
  - manifest.json: post content configuration information (e.g. title)
  - README.rst: reStructuredText content
"""
import os

from django_docutils.exc import BasedException
from django_docutils.lib.fixtures.utils import find_rst_files


def find_series_files(config, path):
    """Find series files from config + path.

    Configs don't hold the path of the files right now, so we pass it in.

    :param config: config.json in dict format
    :type config: :class:`python:dict`
    :param path: path to project (directory)
    :type path: string
    :returns: *ordered* list of files, relative to path
    :rtype: list
    """

    files_in_path = find_rst_files(path, absolute=True)
    files_in_series = [os.path.join(path, f) for f in config["series"]]

    # assert series in config matches files present in directory, if not
    # throw exception
    has_files = set(files_in_path) == set(files_in_series)

    if not has_files:
        raise BasedException(
            "Files in {} ({}) do not match the ones listed in"
            'the "series" metadata ({}).'.format(
                path, ", ".join(files_in_path), ", ".join(files_in_series)
            )
        )

    return files_in_series


def is_dir_project(path):
    """Return True if directory is a directory-based project.

    (As opposed to a single file.)

    :param path: Directory of project
    :type path: string
    :returns; If directory has the proper files to be a "dir"-type project
    :rtype: boolean
    """
    required_files = [
        os.path.join(path, "README.rst"),
        os.path.join(path, "manifest.json"),
    ]

    return all(os.path.exists(f) for f in required_files)


def find_rst_dirs_in_app(app_config):
    """Return reStructuredText fixtures from fixtures dir for app.

    :param app_config: Configuration for django app
    :type app_config: :class:`django.apps.AppConfig`
    :returns: list of files relative to app's fixture dir path
    """
    fixtures_dir = os.path.join(app_config.path, "fixtures")
    return find_rst_dir_projects(fixtures_dir)


def find_rst_dir_projects(path):
    """Find and return projects in a directory with:

    - manifest.json
    - README.rst

    :param path: Path to search for projects
    :type path: string
    :returns: List of directories containing fixtures projects in dir format
    :rtype: list
    """
    paths = []
    for _root, dirname, filenames in os.walk(path):
        for dir_ in dirname:
            if is_dir_project(os.path.join(_root, dir_)):
                paths.append(os.path.join(_root, dir_))
    return paths
