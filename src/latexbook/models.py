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

    # The plain-text, if applicable, attached to this node.
    # I feel like there should be seperate model for TextNode, but I can't figure out
    # how to then 'insert' the text back into the tree - whilst retaining the order.
    content = models.TextField(null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["position"]
