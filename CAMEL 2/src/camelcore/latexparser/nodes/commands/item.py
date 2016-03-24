from latexbook.latexparser.nodes.command import CommandNode


class ItemNode(CommandNode):
    """An abstract item command node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(ItemNode, self).__init__(children=children)


class Item(ItemNode):
    """An item command node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Item, self).__init__(children=children)
