from argparse import FileType

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction

from latexbook.latexparser.texbookparser import TexBookParser
from latexbook.parseradapter import write_to_django_database
from latexbook.models import BookNode

class Command(BaseCommand):
    help = "Parses a LaTeX book file into a Django-friendly form."

    def add_arguments(self, parser):
        """
        Add arguments for this command.
        See the following:
        https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/
        https://docs.python.org/3/library/argparse.html#module-argparse
        """
        parser.add_argument(
            "latex_file", type=FileType("r"),
            help="The LaTeX file to be parsed."
        )

    def handle(self, *args, **options):
        if hasattr(settings, "BOOKNODES"):
            book_nodes = settings.BOOKNODES

            latex_file = options["latex_file"]
            latex_document = latex_file.read()

            parser = TexBookParser(book_nodes)
            book_node = parser.parse(latex_document)

            with transaction.atomic():
                with BookNode.objects.disable_mptt_updates():
                    write_to_django_database(book_node)
                BookNode.objects.rebuild()
        else:
            raise CommandError("BOOKNODES could not be aquired from your settings!")