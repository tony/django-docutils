import fnmatch
import os

from django.apps import apps


def get_model_from_post_app(app_config):
    """Return post model for app.

    :param app_config: Configuration for django app
    :type app_config: :class:`django.apps.AppConfig`
    :returns: Post sub-model for app
    :rtype: Model
    """
    from django_docutils.rst_post.models import RSTPostBase

    for model in app_config.get_models():
        if issubclass(model, RSTPostBase):
            return model


def find_rst_files(path, absolute=False, recursive=False):
    """Find .rst files in directory.

    This is reused in dir-style projects.

    :param path: path to project (directory)
    :type path: string
    :param absolute: return absolute paths
    :type absolute: bool
    :param recursive: recursively check for rst files
    :type recursive: bool
    :returns: return list of .rst files from path
    :rtype: list
    """
    files = []
    for _root, dirname, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.rst'):
            p = os.path.relpath(_root, path)
            if absolute:
                files.append(os.path.normpath(os.path.join(path, p, filename)))
            else:
                files.append(os.path.join(p, filename))
        if not recursive:
            break
    return files


def find_app_configs_with_fixtures(has_rst_files=True):
    """Return a list of apps with fixtures dir.

    In Django 1.11 fixture_dirs grabs a directory of all fixtures, in our
    situation, we want to grab the correct model.

    :param has_rst_files: Only return apps with .rst files in fixtures
    :type has_rst_files: bool
    :returns: list of app configs with fixtures directory
    :rtype: list of :django:class`django.apps.AppConfig`
    """
    app_configs = []
    for app_config in apps.get_app_configs():
        app_dir = os.path.join(app_config.path, 'fixtures')
        if os.path.isdir(app_dir):
            if has_rst_files:
                if len(find_rst_files(app_dir, recursive=True)) < 1:
                    continue
            app_configs.append(app_config)

    return app_configs


def find_rst_files_in_app(app_config):
    """Return fixtures reStructuredText files from fixtures dir for app.

    :param app_config: Configuration for django app
    :type app_config: :class:`django.apps.AppConfig`
    :returns: list of files relative to app's fixtures dir path
    """
    fixtures_dir = os.path.join(app_config.path, 'fixtures')
    return find_rst_files(fixtures_dir)


def split_page_data(post_data):
    """Pluck the page data from the post data and return both.

    publish_post is pure and doesn't know what a post/page is.

    Posts contain pages. devel.tech's architecture needs to split page data
    from the post. The page will store the "body" content and also
    a subtitle.
    """
    page_data = {}
    for field in ['body', 'subtitle', 'draft']:
        try:
            page_data[field] = post_data.pop(field)
        except KeyError:  # handle corner case, no subtitle/body
            pass
    return post_data, page_data
