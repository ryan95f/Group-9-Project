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
    """A leaf node whos parent is BookNode. Contains simply plain-text."""
    # The parent this node belongs to.
    parent = models.ForeignKey(BookNode, blank=True, null=True, on_delete=models.CASCADE)

    # The position in which the node appears inside the parent.
    position = models.IntegerField()

    # The plain-text attached to this leaf-node.
    text = models.TextField()
