import typing as t

SECRET_KEY = "dummy"

DATABASES = {"default": {"NAME": ":memory:", "ENGINE": "django.db.backends.sqlite3"}}

DJANGO_DOCUTILS_LIB_TEXT: t.Dict[str, t.Dict[str, str]] = {}

INSTALLED_APPS = ["django.contrib.contenttypes"]

USE_TZ = False
