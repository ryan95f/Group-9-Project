from latexbook.latexparser.nodes.node import (
    ArgumentNode as OriginalArgumentNode,
    TextNode as OriginalTextNode
)


class ArgumentNode(OriginalArgumentNode):
    """A node which represents an argument for the parent node."""

    def __init__(self, children=None):
        """Initialise the argument node."""
        super(ArgumentNode, self).__init__(children=children)


class TextNode(OriginalTextNode):
    """A leaf node which just holds some plain text."""

    def __init__(self, content):
        """Initialise the text leaf node."""
        super(TextNode, self).__init__(content=content)
