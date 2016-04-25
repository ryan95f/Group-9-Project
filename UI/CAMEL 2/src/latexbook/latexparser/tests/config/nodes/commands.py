from ....nodes.command import CommandNode


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


class TextIt(TextStyle):
    """An italic text command node."""

    def __init__(self, children=None):
        """Initialise the new instance of our class."""
        super(TextIt, self).__init__(children=children)
