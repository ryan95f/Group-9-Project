from latexbook.latexparser.nodes.command import CommandNode


class Item(CommandNode):
    """An item command node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Item, self).__init__(children=children)
