"""A few utilities which are used to help make our LaTeX parser work well with Django."""

from django.conf import settings
from django.db import transaction

from latexbook.latexparser.texbookparser import TexBookParser
from latexbook.models import BookNode, TextNode


def write_document_into_database(latex_document):
    """Parse the given LaTeX document text and write the resulting nodes into the database."""
    book_nodes = settings.BOOKNODES

    parser = TexBookParser(book_nodes)
    book_node = parser.parse(latex_document)

    with transaction.atomic():
        with BookNode.objects.disable_mptt_updates():
            write_node_into_database(book_node)
        BookNode.objects.rebuild()

    return book_node


def write_node_into_database(node, parent_node=None):
    """
    Write a Node, from the latexparser package, into our database.

    We recursively call this function on all the immediate children of the given node - parsing the node itself to each
    call, so the relation between the child and parent may exist bidirectionally.
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
                write_node_into_database(node=child, parent_node=book_node)
