from collections import namedtuple

from django import template
from django.conf import settings

register = template.Library()

@register.assignment_tag
def latex_node_to_html(node):
    """Converts a LaTeX node (from the database) into some HTML."""
    node_object = settings.BOOKNODES.get_class(node.node_type)

    # Check if the node is a 'text' BookNode.
    if node.node_type == settings.BOOKNODES.text_node_id:
        # Checks if this BookNode does actually have a One-to-One relation with TextNode.
        # This should ALWAYS be True, otherwise something has gone wrong!
        if hasattr(node, "text_node"):
            text_node_content = node.text_node.content
            the_node_html = node_object.to_html(text_node_content)

    # Check that the node isn't an argument node (as the parent will handle their display).
    elif node.node_type != settings.BOOKNODES.argument_node_id:
        arguments = node.get_children().filter(node_type=settings.BOOKNODES.argument_node_id)
        the_node_html = node_object.to_html(arguments)
    else:
        the_node_html = node_object.to_html()

    return the_node_html
