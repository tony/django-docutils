# ruff: noqa: PTH112 PTH118
import contextlib
import fnmatch
import os
import typing as t


def find_rst_files(
    path: str, absolute: bool = False, recursive: bool = False
) -> t.List[str]:
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
    for _root, _dirname, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "*.rst"):
            p = os.path.relpath(_root, path)
            if absolute:
                files.append(os.path.normpath(os.path.join(path, p, filename)))
            else:
                files.append(os.path.join(p, filename))
        if not recursive:
            break
    return files


def split_page_data(
    post_data: t.Dict[str, t.Any]
) -> t.Tuple[t.Dict[str, t.Any], t.Dict[str, t.Any]]:
    """Pluck the page data from the post data and return both.

    publish_post is pure and doesn't know what a post/page is.

    Posts contain pages. devel.tech's architecture needs to split page data
    from the post. The page will store the "body" content and also
    a subtitle.
    """
    page_data = {}
    for field in ["body", "subtitle", "draft"]:
        with contextlib.suppress(KeyError):
            page_data[field] = post_data.pop(field)
    return post_data, page_data
