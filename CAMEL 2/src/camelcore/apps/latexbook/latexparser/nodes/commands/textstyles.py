from latexbook.latexparser.nodes.command import CommandNode


class TextStyle(CommandNode):
    """An abstarct text style command node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(TextStyle, self).__init__(children=children)


class TextIt(TextStyle):
    """An italic text command node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(TextIt, self).__init__(children=children)


class TextBf(TextStyle):
    """A bold text command node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(TextBf, self).__init__(children=children)


class Underline(TextStyle):
    """An underlined text command node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Underline, self).__init__(children=children)


class Emph(TextStyle):
    """An emphasising text command node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Emph, self).__init__(children=children)
