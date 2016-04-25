import os

from collections import namedtuple

from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.backends.django import Template
from django.template.context import Context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode, ExtendsNode

register = template.Library()

# Used to store the rendered information for a Django BookNode.
NodeHTML = namedtuple("NodeHTML", "prefix_text suffix_text")


def get_template_node(template, name, context=Context()):
    """
    Iterate through the nodes of the given template and return the contents of the block with the given name.

    It would be neat if this function could handle template inheritence (via extends), but I was unable to get it
    working. I have commented out my attempt.
    """
    for node in template:
        if isinstance(node, BlockNode) and node.name == name:
            return node.render(context)
        # elif isinstance(node, ExtendsNode):
        #     return get_template_node(node.get_parent(), name, context)
    raise ImproperlyConfigured("Unable to find block '%s' within template!" % name)


@register.assignment_tag(takes_context=True)
def latex_node_to_html(context, node):
    """
    Given a Django-MPTT LaTeX node model, this template-tag will return the associated rendered prefix and suffix.

    In Django, it is generally considered "bad-practice" to try a manually dissect blocks from a
    template. However, the alternative is to have two files per LaTeX node (Prefix and Suffix)
    which would make our file structure a mess and full of near-pointless suffix files (consisting
    of just '</div>').
    """
    node_id = node.node_type
    if node_id != settings.BOOKNODES.argument_node_id:
        if node_id in settings.LATEX_NODE_TEMPLATE_PATHS:
            node_template_path = settings.LATEX_NODE_TEMPLATE_PATHS[node_id]

            node_template = get_template(node_template_path).template

            try:
                prefix_rendered_text = get_template_node(node_template, "prefix", context)
            except ImproperlyConfigured:
                prefix_rendered_text = None

            try:
                suffix_rendered_text = get_template_node(node_template, "suffix", context)
            except ImproperlyConfigured:
                suffix_rendered_text = None

            return NodeHTML(prefix_text=prefix_rendered_text, suffix_text=suffix_rendered_text)
        else:
            raise ValueError("Missing template path setting for LaTeX node '{0}'".format(node_id))


@register.filter
def process_children(node):
    """Only process the children of the given node if this boolean equates to True."""
    node_id = node.node_type
    return settings.BOOKNODES.argument_node_id != node_id
