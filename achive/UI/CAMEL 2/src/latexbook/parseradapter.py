"""A few utilities which are used to help make our LaTeX parser work well with Django.

TODO:
    - Figure out an elegant solution to handle the case when commit is False.
"""

from django.conf import settings
from django.db import transaction

from latexbook.latexparser.texbookparser import TexBookParser
from latexbook.models import BookNode, TextNode


def parse_document(latex_document):
    """Parse the given LaTeX document text into LaTeX node objects."""
    parser = TexBookParser(settings.BOOKNODES)
    return parser.parse(latex_document)


def write_node_into_database(root_node, commit=True):
    """Write the given LaTeX parser node, and its children, into the database."""
    with transaction.atomic():
        with BookNode.objects.disable_mptt_updates():
            book_node = __write_node_into_database(node=root_node, commit=commit)
        BookNode.objects.rebuild()

    return book_node


def __write_node_into_database(node, parent_node=None, commit=True):
    """Internal function which writes a LaTeX parser node into the database.

    All decendents of the given node into the database through recursion.
    """
    content = node.content if hasattr(node, "content") else None

    node_type = node.get_id()

    # Create BookNode model instance for the current node.
    book_node = BookNode.objects.create(
        parent=parent_node,
        position=node.position,
        node_type=node_type
    )
    book_node.save()

    # As we store the plain-text contents of a TextNode using a seperate model,
    # we check if the current node is a TextNode and create it accordingly.
    if node_type == settings.BOOKNODES.text_node_id:
        text_node = TextNode(
            book_node=book_node,
            content=content
        )
        text_node.save()
    else:
        # A non-text node could have children, so make a recursive call.
        if hasattr(node, "children"):
            for child in node.children:
                __write_node_into_database(node=child, parent_node=book_node, commit=commit)

    return book_node
