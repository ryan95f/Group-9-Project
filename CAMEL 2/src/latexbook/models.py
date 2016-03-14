from django.db import models

# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey


class BookNode(MPTTModel):
    """Represents a node inside a book."""

    # The parent this node belongs to.
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
        on_delete=models.CASCADE
    )

    # The position in which the node appears inside the parent.
    position = models.IntegerField()

    # The type of this node. e.g. Chapter, Section, Verbatim, TextIt, ArgumentNode etc...
    node_type = models.CharField(max_length=50)

    def __str__(self):
        return self.node_type

    class MPTTMeta:
        order_insertion_by = ["position"]


class TextNode(models.Model):
    """Associates some plain-text to a 'text' node from the BookNode model."""

    # The id of the 'text' node in the BookNode model.
    book_node = models.OneToOneField(
        BookNode,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="text_node"
    )

    # The actual plain-text for the node.
    content = models.TextField()

    def __str__(self):
        return self.content


class Book(models.Model):
    """
    A wrapper for BookNode's of the type 'book'.

    This allows us to attach some meta-data for each of our books.
    It would be better if this model didn't exist and we instead dfined the meta-data within our LaTeX files;
    cpaturing the data as ArgumentNodes.
    """

    book_root_node = models.OneToOneField(
        BookNode,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="book"
    )

    title = models.CharField(max_length=64)

    # Preferably, this would be a ManyToMany relation to teacher users.
    author = models.CharField(max_length=64)

    def __str__(self):
        return self.title + " by " + self.author
