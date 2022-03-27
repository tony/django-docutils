from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections, transaction

from django_docutils.references.intersphinx.load import load_mappings


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
        load_mappings()
