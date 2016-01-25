from latexbook.models import BookNode

def write_to_django_database(node, parent_node=None):
    """
    Writes the book (which is a tree data structure) into the Django database.
    This function adds the children of 'node' through recursive calls.
    """
    content = node.content if hasattr(node, "content") else None

    book_node = BookNode.objects.create(
        parent=parent_node,
        position=node.position,
        node_type=node.get_id(),
        content=content
    )

    # Save to Django database.
    book_node.save()

    # Although a TextNode can't have children, a regular node could have.
    if hasattr(node, "children"):
        for child in node.children:
            write_to_django_database(node=child, parent_node=book_node)
