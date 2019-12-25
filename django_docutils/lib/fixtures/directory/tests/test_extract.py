import datetime

import py

from django_docutils.lib.fixtures.directory.extract import extract_dir_config
from django_docutils.lib.metadata.process import process_metadata


def test_extract_dir_config(sample_dir_app_config):
    sample_dir_app_dir = py.path.local(sample_dir_app_config.path)
    project_dir = sample_dir_app_dir.join('fixtures').join('sample_project')

    raw_metadata = extract_dir_config(str(project_dir))
    analyzed_metadata = process_metadata(raw_metadata.copy())

    assert isinstance(analyzed_metadata['created'], datetime.date)

    assert process_metadata(raw_metadata) != {
        'programming_languages': ['python'],
        'topics': ['Web Frameworks'],
        'created': '2017-09-12',
        'author': 'tony',
    }
