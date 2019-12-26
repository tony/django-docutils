import pytest

# from django.apps import apps


def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage',
        FAVICON_MODEL='django_docutils.favicon.tests.test_app.models.Favicon',
        REFERENCE_MODEL='django_docutils.favicon.tests.test_app.models.Reference',
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}
        },
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            },
        ],
        BASED_LIB_RST={
            'metadata_processors': [
                'django_docutils.lib.metadata.processors.process_datetime',
                'django_docutils.lib.metadata.processors.process_anonymous_user',
                'django_docutils.lib.metadata.processors.process_m2m_fields',
            ],
            'transforms': [  #: docutils.transforms.Transform class (import string)
                'django_docutils.references.rst.transforms.xref.XRefTransform',
                'django_docutils.favicon.rst.transforms.favicon.FaviconTransform',
                'django_docutils.lib.transforms.code.CodeTransform',
            ],
            'docutils': {  #: Used in restructuredtext templatetags
                'raw_enabled': True,
                'strip_comments': True,
                'initial_header_level': 2,
            },
            'directives': {  #: directive-name: Directive class (import string)
                'code-block': 'django_docutils.lib.directives.code.CodeBlock'
            },
            'roles': {
                'local': {
                    'gh': 'django_docutils.lib.roles.github.github_role',
                    'pypi': 'django_docutils.lib.roles.pypi.pypi_role',
                    'kbd': 'django_docutils.lib.roles.kbd.kbd_role',
                    'file': 'django_docutils.lib.roles.file.file_role',
                    'exe': 'django_docutils.lib.roles.file.exe_role',
                    'manifest': 'django_docutils.lib.roles.file.manifest_role',
                    'amzn': 'django_docutils.lib.roles.amazon.amazon_role',
                    'rtd': 'django_docutils.lib.roles.readthedocs.readthedocs_role',
                    'url': 'django_docutils.lib.roles.url.url_role',
                    'leanpub': 'django_docutils.lib.roles.leanpub.leanpub_role',
                    'twitter': 'django_docutils.lib.roles.twitter.twitter_role',
                    'email': 'django_docutils.lib.roles.email.email_role',
                    'hn': 'django_docutils.lib.roles.hackernews.hackernews_role',
                    'wikipedia': 'django_docutils.lib.roles.wikipedia.wikipedia_role',
                    'site_url': 'django_docutils.lib.roles.develtech.site_url_role',
                    'post:snippet': 'django_docutils.lib.roles.develtech.post_role',
                    'post:tip': 'django_docutils.lib.roles.develtech.post_role',
                    # Cross-reference stuff
                    'doc': (
                        'django_docutils.references.rst.roles.XRefRole',
                        {
                            'innernodeclass': 'docutils.nodes.inline',
                            'warn_dangling': True,
                        },
                    ),
                    'ref': (
                        'django_docutils.references.rst.roles.XRefRole',
                        {
                            'lowercase': True,
                            'innernodeclass': 'docutils.nodes.inline',
                            'warn_dangling': True,
                        },
                    ),
                    'class': 'django_docutils.references.rst.roles.PyXRefRole',
                    'meth': (
                        'django_docutils.references.rst.roles.PyXRefRole',
                        {'fix_parens': True},
                    ),
                    'func': (
                        'django_docutils.references.rst.roles.PyXRefRole',
                        {'fix_parens': True},
                    ),
                    'exc': 'django_docutils.references.rst.roles.PyXRefRole',
                    'envvar': 'django_docutils.references.rst.roles.PyXRefRole',
                    'data': 'django_docutils.references.rst.roles.PyXRefRole',
                    'attr': 'django_docutils.references.rst.roles.PyXRefRole',
                }
            },
        },
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'django_extensions',
            'django_docutils.favicon.tests.test_app',
            'guardian',
        ),
        PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',),
        USE_TZ=True,
        ANONYMOUS_USER_NAME='AnonymousCoward',
        GUARDIAN_GET_INIT_ANONYMOUS_USER='django_docutils.rst_post.models.get_anonymous_user_instance',
        GUARDIAN_MONKEY_PATCH=False,
    )

    try:
        import django

        django.setup()
    except AttributeError:
        pass


@pytest.fixture(scope='session', autouse=True)
def django_db_use_migrations():
    return False


# @pytest.fixture(autouse=True)
# def favicon_app(settings, request, django_db_use_migrations):
#     app_name = 'test_app'
#     app_import_string = f'django_docutils.favicon.tests.{app_name}'
#
#     if app_import_string not in settings.INSTALLED_APPS:
#         settings.INSTALLED_APPS = settings.INSTALLED_APPS + (app_import_string,)
#
#     def resource_a_teardown():
#         print('\nresources_a_teardown()')
#         settings.INSTALLED_APPS = (
#             s for s in settings.INSTALLED_APPS if s != app_import_string
#         )
#
#         assert app_import_string not in settings.INSTALLED_APPS
#
#     request.addfinalizer(resource_a_teardown)
#
#     return apps.get_app_config(app_name)