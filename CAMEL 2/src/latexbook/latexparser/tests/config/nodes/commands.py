from ....nodes.command import CommandNode
from ....nodes.node import NodeHTML


class TextStyle(CommandNode):
    """An abstarct text style command node."""

    def __init__(self, children=None):
        """Initialise the new instance of our class."""
        super(TextStyle, self).__init__(children=children)


class Emph(TextStyle):
    """An emphasising text command node."""

    def __init__(self, children=None):
        """Initialise the new instance of our class."""
        super(Emph, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<em class='latex_command_emph'>",
            process_children=True,
            suffix_text="</em>"
        )


class TextIt(TextStyle):
    """An italic text command node."""

    def __init__(self, children=None):
        """Initialise the new instance of our class."""
        super(TextIt, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<i class='latex_command_textit'>",
            process_children=True,
            suffix_text="</i>"
        )
