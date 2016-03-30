from argparse import FileType

from django.core.management.base import BaseCommand
from latexbook.parseradapter import write_document_into_database


class Command(BaseCommand):
    """A command for parsing LaTeX files into the LaTeX parser then writing the result into the database."""

    help = "Parses a LaTeX book file into the LaTeX parser then writes the resulting nodes into the database"

    def add_arguments(self, parser):
        """Add arguments for this command.

        See the following:
        https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/
        https://docs.python.org/3/library/argparse.html#module-argparse
        """
        parser.add_argument(
            "latex_file", type=FileType("r"),
            help="The LaTeX file to be parsed."
        )

    def handle(self, *args, **options):
        """Called when the command is executed and ready to be handled."""
        latex_file = options["latex_file"]
        latex_document = latex_file.read()
        write_document_into_database(latex_document)
