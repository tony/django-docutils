import pytest

# from django.apps import apps


def pytest_configure():
    from django.conf import settings

    settings.configure(
        FAVICON_MODEL='django_docutils.favicon.tests.test_app.models.Favicon',
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
            'django_docutils.favicon.tests.test_app',
        ),
        PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',),
        USE_TZ=True,
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
