from latexbook.models import BookNode, TextNode

def write_to_django_database(nodes, node, parent_node=None):
    """
    Writes the book (which is a tree data structure) into the Django database.
    This function adds the children of 'node' through recursive calls.
    """
    # Check if the node is a TextNode.
    if node.text_node_id == node.get_id():
        text_node = TextNode.objects.create(parent=parent_node, position=node.position, text=node.content)

        # Save to Django database.
        text_node.save()
    else:
        book_node = BookNode.objects.create(parent=parent_node, position=node.position, node_type=node.get_type())

        # Save to Django database.
        book_node.save()

        # Although a TextNode can't have children, a regular node could have.
        for child in node.children:
             write_to_django_database(nodes=nodes, node=child, parent=book_node)
