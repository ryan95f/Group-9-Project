from collections import namedtuple

from django import template

register = template.Library()

NodeHTML = namedtuple("NodeHTML", "prefix_text process_children suffix_text")

@register.assignment_tag
def latex_node_to_html(node):
	"""Converts a LaTeX node (from the database) into some HTML."""
	the_node_html = NodeHTML(prefix_text="", process_children=True, suffix_text="")

	if node.node_type == "text":
		the_node_html = NodeHTML(
			prefix_text = "<span>" + node.content,
			process_children = False,  # Not strickly required as a text node will NEVER have children.
			suffix_text = "</span>"
		)
	elif not node.is_leaf_node():
		the_node_html = NodeHTML(
			prefix_text = "<div class=" + node.node_type + ">",
			process_children = True,
			suffix_text = "</div>"
		)
	return the_node_html