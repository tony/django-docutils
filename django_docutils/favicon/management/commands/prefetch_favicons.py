from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections, transaction

from django_docutils.lib.favicon.prefetch import prefetch_favicons

from ...models import get_favicon_model


class Command(BaseCommand):
    help = "Parse all page/node content for favicons."

    def handle(self, **options):
        if options["clear"]:
            self.stdout.write("Wiping favicons")
            Favicon = get_favicon_model()
            for f in Favicon.objects.all():
                f.delete()

        self.using = options["database"]
        self.url_pattern = options["pattern"]

        with transaction.atomic(using=self.using):
            prefetch_favicons(self.url_pattern)

        # Close the DB connection -- unless we're still in a transaction. This
        # is required as a workaround for an  edge case in MySQL: if the same
        # connection is used to create tables, load data, and query, the query
        # can return incorrect results. See Django #7572, MySQL #37735.
        if transaction.get_autocommit(self.using):
            connections[self.using].close()

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--clear",
            action="store_true",
            dest="clear",
            help="Clear the existing favicons from the database"
            "before trying to fetch favicons.",
        )

        parser.add_argument(
            "--database",
            action="store",
            dest="database",
            default=DEFAULT_DB_ALIAS,
            help="Nominates a specific database to load fixtures into. "
            'Defaults to the "default" database.',
        )

        parser.add_argument(
            "--pattern",
            action="store",
            dest="pattern",
            default=None,
            help="Only parse URL's with pattern",
        )
