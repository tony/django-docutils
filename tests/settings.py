"""django-docutils test settings module for django."""
import pathlib
import typing as t

import django

if t.TYPE_CHECKING:
    from django_docutils.lib.types import DjangoDocutilsLibRSTSettings

if django.VERSION <= (4, 2):
    USE_L10N = True

if django.VERSION <= (4, 1):
    DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"
else:
    STORAGES = {
        "default": {
            "BACKEND": "inmemorystorage.InMemoryStorage",
        },
    }

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
SECRET_KEY = "not very secret in tests"
USE_TZ = True
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [pathlib.Path(__file__).parent / "templates"],
    },
    {
        "NAME": "docutils",
        "BACKEND": "django_docutils.template.DocutilsTemplates",
        "APP_DIRS": True,
        "DIRS": [pathlib.Path(__file__).parent / "rst_content"],
    },
]
DJANGO_DOCUTILS_ANONYMOUS_USER_NAME = "AnonymousCoward"
DJANGO_DOCUTILS_LIB_RST: "DjangoDocutilsLibRSTSettings" = {
    "metadata_processors": [
        "django_docutils.lib.metadata.processors.process_datetime",
        "django_docutils.lib.metadata.processors.process_anonymous_user",
    ],
    "transforms": [  #: docutils.transforms.Transform class (import string)
        "django_docutils.lib.transforms.code.CodeTransform",
    ],
    "docutils": {  #: Used in restructuredtext templatetags
        "raw_enabled": True,
        "strip_comments": True,
        "initial_header_level": 2,
    },
    "directives": {  #: directive-name: Directive class (import string)
        "code-block": "django_docutils.lib.directives.code.CodeBlock",
    },
    "roles": {
        "local": {
            "gh": "django_docutils.lib.roles.github.github_role",
            "pypi": "django_docutils.lib.roles.pypi.pypi_role",
            "kbd": "django_docutils.lib.roles.kbd.kbd_role",
            "file": "django_docutils.lib.roles.file.file_role",
            "exe": "django_docutils.lib.roles.file.exe_role",
            "manifest": "django_docutils.lib.roles.file.manifest_role",
            "rtd": "django_docutils.lib.roles.readthedocs.readthedocs_role",
            "url": "django_docutils.lib.roles.url.url_role",
            "leanpub": "django_docutils.lib.roles.leanpub.leanpub_role",
            "twitter": "django_docutils.lib.roles.twitter.twitter_role",
            "email": "django_docutils.lib.roles.email.email_role",
            "hn": "django_docutils.lib.roles.hackernews.hackernews_role",
            "wikipedia": "django_docutils.lib.roles.wikipedia.wikipedia_role",
        },
    },
}
DJANGO_DOCUTILS_LIB_TEXT: t.Dict[str, t.List[str]] = {  # Optional
    "uncapitalized_word_filters": ["project.my_module.my_capitalization_fn"],
}
INSTALLED_APPS = ("django_docutils",)
