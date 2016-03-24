from camelcore.latexbook.latexparser.nodes.commands.item import ItemNode


class Choice(ItemNode):
    """Represents a choicer in a homework quiz question."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Choice, self).__init__(children=children)


class CorrectChoice(ItemNode):
    """Represents a correct choice for a homework quiz question."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(CorrectChoice, self).__init__(children=children)


class TextAnswer(ItemNode):
    """Represents a text-based answer for a homework quiz question."""

    allowed_children = False  # Don't parse the contents!

    def __init__(self, children=None):
        """Initialise the node."""
        super(TextAnswer, self).__init__(children=children)
