from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections, transaction

from django_docutils.lib.directives import register_based_directives
from django_docutils.lib.fixtures.load import load_app_rst_fixtures
from django_docutils.lib.fixtures.utils import find_app_configs_with_fixtures
from django_docutils.lib.roles import register_based_roles

User = get_user_model()


class Command(BaseCommand):
    help = "Installs / Updates growth rst file(s) in the database."

    def handle(self, **options):
        self.using = options["database"]
        with transaction.atomic(using=self.using):
            self.loaddata()

        # Close the DB connection -- unless we're still in a transaction. This
        # is required as a workaround for an  edge case in MySQL: if the same
        # connection is used to create tables, load data, and query, the query
        # can return incorrect results. See Django #7572, MySQL #37735.
        if transaction.get_autocommit(self.using):
            connections[self.using].close()

    def add_arguments(self, parser):
        parser.add_argument(
            "--database",
            action="store",
            dest="database",
            default=DEFAULT_DB_ALIAS,
            help="Nominates a specific database to load fixtures into. "
            'Defaults to the "default" database.',
        )

    def loaddata(self):
        # prepare directives / roles
        register_based_directives()
        register_based_roles()

        # apps that have growth fixtures
        app_configs = find_app_configs_with_fixtures(has_rst_files=True)

        for app_config in app_configs:
            load_app_rst_fixtures(app_config=app_config)
