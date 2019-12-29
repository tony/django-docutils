"""Metadata is a catch-all term for information for an RST document.

It can be pulled from the RST file itself, such as:

- The Title/Subtitle of the document
- The docinfo attributes

In the case of directory-style projects, the manifest.json.

These optional pipeline functions can be configured to to create, read,
update, and delete metadata from RST projects.

To set metadata processors, use BASED_LIB_RST['metadata_processors']::

    BASED_LIB_RST = {
        'metadata_processors': [
            'django_docutils.lib.metadata.processors.process_datetime'
        ],
    }

The order of the processors will be respected.

The function accepts one argument, the metadata dictionary, and returns the
same dictionary::

    def process_datetime(metadata):
        # create, read, update, delete metadata from the RST document
        return metadata

See *processors.py* for more examples.
"""
from django.utils.module_loading import import_string

from ..settings import BASED_LIB_RST


def process_metadata(metadata):
    """Return objects from rst metadata pulled from document source.

    This will turn things like string dates into time-zone'd dateutil objects.

    :param metadata: data returned from processing an RST file
    :type metadata: dict
    :rtype: dict
    """

    if not BASED_LIB_RST:
        return metadata

    if 'metadata_processors' in BASED_LIB_RST:
        for processor_str in BASED_LIB_RST['metadata_processors']:
            processor_fn = import_string(processor_str)
            metadata = processor_fn(metadata)

    return metadata
