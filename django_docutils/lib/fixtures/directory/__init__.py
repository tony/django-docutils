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
  - manifest.json: post content configuration information (e.g. title, taxonomy)
  - README.rst: reStructuredText content
"""
