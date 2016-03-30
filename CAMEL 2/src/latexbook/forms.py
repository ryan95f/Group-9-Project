from django.forms import FileField, Form, ModelForm

from latexbook.models import Book
from latexbook.parseradapter import write_document_into_database


class BookForm(ModelForm):
    """Create a new book from a LaTeX file."""

    class Meta:
        """The Meta class for our form."""

        model = Book
        exclude = ("book_root_node",)


class BookNodeForm(Form):
    """Upload a LaTeX file and write it its content into the database.."""

    latex_file = FileField()

    def save(self):
        """Parse the contents of the uploaded LaTeX file and write the resulting BookNodes into the database."""
        latex_file = self.cleaned_data["latex_file"]
        latex_document = latex_file.read().decode("ascii")
        book_node = write_document_into_database(latex_document)
        return book_node
