import json
import os


def extract_dir_config(path):
    """Return config metadata for dir RST project.

    Automatically lowercases keys for a parity with docutils' docinfo behavior.

    :param path: path to project (directory)
    :type path: string
    :returns: metadata from json file
    :rtype: dict
    """
    config_file = os.path.join(path, 'manifest.json')
    config_dict = json.loads(open(config_file).read())
    return {k.lower(): v for k, v in config_dict.items()}
