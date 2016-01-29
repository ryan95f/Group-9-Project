from django.conf import settings

from latexbook.models import BookNode, TextNode

def write_to_django_database(node, parent_node=None):
    """
    Writes the book (which is a tree data structure) into the Django database.
    This function adds the children of 'node' through recursive calls.
    """
    content = node.content if hasattr(node, "content") else None

    node_type = node.get_id()

    book_node = BookNode.objects.create(
        parent=parent_node,
        position=node.position,
        node_type=node_type
    )

    # Save to Django database.
    book_node.save()

    # If this node is a 'text' node, insert its content into the TextNode model.
    if node_type == settings.BOOKNODES.text_node_id:
        text_node = TextNode(
            book_node=book_node,
            content=content
        )
        text_node.save()
    else:
        # A non-text node could have children.
        if hasattr(node, "children"):
            for child in node.children:
                write_to_django_database(node=child, parent_node=book_node)
