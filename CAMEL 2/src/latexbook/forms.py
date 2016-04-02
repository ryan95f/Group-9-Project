from django.forms import FileField, Form, ModelForm

from latexbook.models import Book
from latexbook.parseradapter import parse_document, write_node_into_database


class BaseBookFormMixin(ModelForm):
    """A form for creating a new book."""

    class Meta:
        """The Meta class for our form."""

        model = Book
        exclude = ("book_root_node",)


class BaseLatexFormMixin(Form):
    """A form mixin for uploading a LaTeX file and writing the contents into the database."""

    # The user is to upload a LaTeX file which we shall then parse.
    latex_file = FileField()

    def clean_latex_file(self):
        """Parse the contents of the LaTeX file and return the document root node."""
        latex_file = self.cleaned_data["latex_file"]
        latex_document = latex_file.read().decode("ascii")
        parser_node = parse_document(latex_document)
        return parser_node


class LatexBookForm(BaseBookFormMixin, BaseLatexFormMixin):
    """A form for creating a new book based upon an uploaded LaTeX file."""

    def save(self, commit=True):
        """Save the Model instances."""
        new_book = super(LatexBookForm, self).save(commit=commit)

        parser_node = self.cleaned_data["latex_file"]
        root_node = write_node_into_database(root_node=parser_node, commit=commit)
        new_book.book_root_node = root_node

        if commit:
            new_book.save()

        return new_book
