from django.apps import AppConfig


class TestAppConfig(AppConfig):
    name = 'django_docutils.favicon.tests.test_app'
    label = 'test_app'
    verbose_name = "For pytest"
