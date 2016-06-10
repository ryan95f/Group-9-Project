from latexbook.latexparser.nodes.environment import EnvironmentNode


class ListEnvironmentNode(EnvironmentNode):
    """An abstract node which represents a list environment."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(ListEnvironmentNode, self).__init__(children=children)


class Itemize(ListEnvironmentNode):
    """An unordered list environment."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Itemize, self).__init__(children=children)


class Enumerate(ListEnvironmentNode):
    """An ordered list environment."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Enumerate, self).__init__(children=children)
