from argparse import FileType

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from latexbook.latexparser.texbookparser import TexBookParser
from latexbook.parseradapter import write_to_django_database

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
        book_nodes = settings.BOOKNODES

        latex_file = options["latex_file"]
        latex_document = latex_file.read()

        nodes = build_default_nodes()
        parser = TexBookParser(book_nodes)
        book_node = parser.parse(latex_document)

        write_to_django_database(book_nodes, book_node)
