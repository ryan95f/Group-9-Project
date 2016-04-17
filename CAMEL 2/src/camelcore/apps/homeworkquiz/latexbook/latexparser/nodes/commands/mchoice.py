from camelcore.apps.latexbook.latexparser.nodes.commands.item import ItemNode


class MChoice(ItemNode):
    """Represents a choicer in a multiple-choice homework quiz question."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(MChoice, self).__init__(children=children)


class MCorrectChoice(ItemNode):
    """Represents a correct choice for a multiple-choice homework quiz question."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(MCorrectChoice, self).__init__(children=children)
