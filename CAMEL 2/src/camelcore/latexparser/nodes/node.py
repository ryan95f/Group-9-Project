from latexbook.latexparser.nodes.node import (
    ArgumentNode as OriginalArgumentNode,
    TextNode as OriginalTextNode,
    NodeHTML
)


class ArgumentNode(OriginalArgumentNode):
    """A node which represents an argument for the parent node."""

    def __init__(self, children=None):
        """Initialise the argument node."""
        super(ArgumentNode, self).__init__(children=children)

    @classmethod
    def to_html(self, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(prefix_text=None, process_children=False, suffix_text=None)


class TextNode(OriginalTextNode):
    """A leaf node which just holds some plain text."""

    def __init__(self, content):
        """Initialise the text leaf node."""
        super(TextNode, self).__init__(content=content)

    @classmethod
    def to_html(self, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text=str(arguments),
            process_children=False,
            suffix_text=None
        )