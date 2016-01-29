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


class Module(models.Model):
    """A module."""

    code = models.CharField(primary_key=True, max_length=6)

    title = models.CharField(max_length=64)


class Book(models.Model):
    """A book."""
    title = models.CharField(max_length=64)

    # Preferably, this would be a ManyToMany relation to teacher users.
    author = models.CharField(max_length=64)

    # We use ManyToMany as a Book could be in multiple modules and a module can
    # have multiple books.
    module_codes = models.ManyToManyField(Module)

    book_root_node = models.OneToOneField(
        BookNode,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="book"
    )