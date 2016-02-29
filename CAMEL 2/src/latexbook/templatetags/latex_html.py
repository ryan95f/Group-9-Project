import os

from collections import namedtuple

from django import template
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode

register = template.Library()

NodeHTML = namedtuple("NodeHTML", "prefix_text suffix_text")

@register.assignment_tag(takes_context=True)
def latex_node_to_html(context, node):
    """
    Given a Django-MPTT LaTeX node model, this template-tag will return the associated rendered
    prefix and suffix.

    In Django, it is generally considered "bad-practice" to try a manually dissect blocks from a
    template. However, the alternative is to have two files per LaTeX node (Prefix and Suffix)
    which would make our file structure a mess and full of near-pointless suffix files (consisting
    of just '</div>').
    """
    node_id = node.node_type
    if node_id != settings.BOOKNODES.argument_node_id:
        if node_id in settings.LATEX_NODE_TEMPLATE_PATHS:
            node_template_path = os.path.join(settings.LATEX_NODE_TEMPLATE_PATHS[node_id], node_id) + ".html"

            prefix_rendered_text = None
            suffix_rendered_text = None

            node_template = get_template(node_template_path)
            for node in node_template.template:
                if isinstance(node, BlockNode):
                    if node.name == "prefix":
                        prefix_rendered_text = node.render(context)
                    elif node.name == "suffix":
                        suffix_rendered_text = node.render(context)

            return NodeHTML(prefix_text=prefix_rendered_text, suffix_text=suffix_rendered_text)
        else:
            raise ValueError("Missing template path setting for LaTeX node '{0}'".format(node_id))

@register.filter
def process_children(node):
    """Only process the children of the given node if this boolean equates to True."""
    node_id = node.node_type
    return settings.BOOKNODES.argument_node_id != node_id