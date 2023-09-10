def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage",
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
        SITE_ID=1,
        SECRET_KEY="not very secret in tests",
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
        STATIC_URL="/static/",
        ROOT_URLCONF="tests.urls",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
            },
        ],
        DJANGO_DOCUTILS_LIB_RST={
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
                "code-block": "django_docutils.lib.directives.code.CodeBlock"
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
                    "site_url": "django_docutils.lib.roles.develtech.site_url_role",
                }
            },
        },
        MIDDLEWARE_CLASSES=(
            "django.middleware.common.CommonMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ),
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.staticfiles",
            "django_extensions",
        ),
        PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
        ANONYMOUS_USER_NAME="AnonymousCoward",
    )

    try:
        import django

        django.setup()
    except AttributeError:
        pass
